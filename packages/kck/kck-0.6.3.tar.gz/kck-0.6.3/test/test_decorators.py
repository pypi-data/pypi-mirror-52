import pytest
import datetime
from unittest import mock
import itertools
import time

from random import randint

from kck.lib.decorators import kckprime, kckrefresh
from kck.lib.kck_cache import KCKCache
from kck.lib.kck_database import KCKDatabase
from kck.test.test_case import BaseBlankCassandraTestCase, BaseEnvironmentCheckingTestCase, BaseKCKTestCase

# --- SIMPLE FUNCTIONS FOR TESTING
drunkard_total_counter = 0


# define the querying function
def get_drunkard(establishment_name):
    global drunkard_total_counter
    drunkard_total_counter += 1
    results = KCKDatabase.query(
        "test",
        "select name from drunkards where establishment = :establishment",
        dict(establishment=establishment_name)).fetchall()
    if results:
        return results[0][0]
    return None


# define a function that updates underlying data for the
# querying function above
def add_drunkard(alt_est_name, drunk_name):
    return KCKDatabase.query("test",
                             "insert into drunkards (name, establishment)" +
                             " values " + "(:name, :establishment)", {
                                 "name": drunk_name,
                                 "establishment": alt_est_name
                             })


# define another function that updates underlying data for the
# querying function above
def update_drunkard(alt_est_name, drunk_name):
    return KCKDatabase.query(
        "test",
        "update drunkards set name=:name where establishment=:establishment", {
            "name": drunk_name,
            "establishment": alt_est_name
        })


# define the decorated version of the querying function
# (just call the non-decorated version)
@kckprime(name="drunkard-by-establishment", keys=["establishment_name"])
def decorated_get_drunkard(establishment_name):
    return get_drunkard(establishment_name)


# define the decorated version of the updating function
# (just call the non-decorated version)
@kckrefresh(
    name="drunkard-by-establishment",
    keys=["establishment_name"],
    param_keys={"establishment_name": "alt_est_name"},
    compute=get_drunkard)
def decorated_add_drunkard(alt_est_name, drunk_name):
    add_drunkard(alt_est_name, drunk_name)


# define the decorated version of the 2nd updating function
@kckrefresh(
    name="drunkard-by-establishment",
    keys=["establishment_name"],
    param_keys={"establishment_name": "alt_est_name"},
    compute=get_drunkard)
def decorated_update_drunkard(alt_est_name, drunk_name):
    update_drunkard(alt_est_name, drunk_name)


# define the decorated version of the 2nd updating function that queues a refresh
# request, but doesn't actually perform the refresh
@kckrefresh(
    name="drunkard-by-establishment",
    keys=["establishment_name"],
    param_keys={"establishment_name": "alt_est_name"},
    compute=get_drunkard,
    queued=True)
def decorated_update_drunkard__queued_refresh(alt_est_name, drunk_name):
    update_drunkard(alt_est_name, drunk_name)


no_param_counter = 0


@kckprime(name='test_no_param_function')
def no_param_function():
    global no_param_counter
    time.sleep(0.1)
    if no_param_counter == 0:
        no_param_counter = 1
    else:
        no_param_counter += 1

    return no_param_counter


def no_param_val(val=None):
    global no_param_counter
    if val is not None:
        no_param_counter = val
    return no_param_counter


@kckrefresh(name='test_no_param_function')
def update_param_value(val):
    global no_param_counter
    no_param_counter = val


def sim_cache_entry_99(*args, **kwargs):
    return {'success': True, 'value': 99}


class TestMinimalDecorators(BaseKCKTestCase, BaseBlankCassandraTestCase, BaseEnvironmentCheckingTestCase):

    def setup_method(self, method):
        global no_param_counter
        self.setup_cassandra()
        KCKCache.get_instance(inhibit_framework_registration=True, new_instance=True)
        no_param_counter = 0

    def test_no_param_function_caches(self):
        """
        test that the first call actually calls the function and that the second uses the cache entry
        """
        assert (no_param_function() == 1)

        with mock.patch('kck.lib.kck_cache.KCKCache.get', side_effect=sim_cache_entry_99) as mock_cache_get:
            assert (no_param_function() == 99)
            assert (mock_cache_get.call_count > 0)
            assert (mock_cache_get.call_args_list[0][0][0] == 'test_no_param_function')

    def test_minimal_refresh(self):
        start1 = datetime.datetime.utcnow()
        assert (no_param_function() == 1)
        end1 = datetime.datetime.utcnow()

        start2 = datetime.datetime.utcnow()
        assert (no_param_function() == 1)
        end2 = datetime.datetime.utcnow()

        update_param_value(2)

        start3 = datetime.datetime.utcnow()
        assert (no_param_function() == 3)
        end3 = datetime.datetime.utcnow()

        num_secs_1 = (end1 - start1).total_seconds()
        num_secs_2 = (end2 - start2).total_seconds()
        num_secs_3 = (end3 - start3).total_seconds()

        # test that:
        #   the first call takes longer than a tenth of a second
        #   the second call takes less than a tenth of a second
        #   the second call takes less than half as much time as the first
        assert (num_secs_1 >= 0.1)
        assert (num_secs_2 < 0.1)
        assert (num_secs_2/num_secs_1 < 0.8)
        assert (num_secs_3 < 0.1)
        assert (num_secs_3/num_secs_1 < 0.8)


class TestDecorators(BaseKCKTestCase, BaseBlankCassandraTestCase, BaseEnvironmentCheckingTestCase):
    def setup_method(self, method):
        """clean things up for the tests"""
        global drunkard_total_counter

        # zero out the counter used to determine how many times
        # the primer function has been called
        drunkard_total_counter = 0

        # drop and recreate the drunkards table
        KCKDatabase.query("test", "drop table if exists drunkards")
        KCKDatabase.query("test", """
                create table drunkards (
                    id serial,
                    name varchar(256),
                    establishment varchar(256)
                )
            """)

        self.setup_cassandra()

        KCKCache.get_instance(inhibit_framework_registration=True, new_instance=True)

    def test_primer_primes(self):
        """
        test that the kckprimer decorator is properly subbing cache gets
        for the code in the primer function
        """
        global drunkard_total_counter

        # insert a record in the table
        KCKDatabase.query(
            "test",
            "insert into drunkards (name, establishment) values (:name, :establishment)",
            {
                "name": "Barney",
                "establishment": "Moe's"
            })

        # the querying function shouldn't have been called at all at this point,
        # confirm counter is zero
        assert (drunkard_total_counter == 0)

        # call the querying function directly and verify that the counter has
        # incremented as expected
        assert (get_drunkard("Moe's") == "Barney")
        assert (drunkard_total_counter == 1)

        # call the decorated querying function and verify that the counter
        # has incremented as expected (cache miss)
        assert (decorated_get_drunkard("Moe's") == "Barney")
        assert (drunkard_total_counter == 2)

        # call the decorated querying function and verify that the counter
        # has not incremented (cache hit)
        assert (decorated_get_drunkard("Moe's") == "Barney")
        assert (drunkard_total_counter == 2)

    def test_refresh_refreshes(self):
        """
        test that the kckrefresh decorator refreshes the cache entry as expected
        """

        global drunkard_total_counter

        # the querying function shouldn't have been called at all at this point,
        # confirm counter is at zero
        assert (drunkard_total_counter == 0)

        # call the non-decorated version of the updating function and
        # confirm that the counter is still zero
        add_drunkard(alt_est_name="Moe's", drunk_name="Barney")
        assert (drunkard_total_counter == 0)

        # call the non-decorated version of the querying function and
        # confirm that the counter increments as expected
        assert (get_drunkard("Moe's") == "Barney")
        assert (drunkard_total_counter == 1)

        # call the decorated version of the updating function and
        # confirm the counter incremements as it should if, just
        # after the new record was added, the cache refreshed
        decorated_add_drunkard(alt_est_name="Cheers", drunk_name="Norm")
        assert (drunkard_total_counter == 2)

        # call the decorated querying function for the record just added
        # and confirm that the counter did not increment, indicating a
        # successful cache hit
        assert (decorated_get_drunkard("Cheers") == "Norm")
        assert (drunkard_total_counter == 2)

        # call the decorated querying function, confirm increment
        assert (decorated_get_drunkard("Moe's") == "Barney")
        assert (drunkard_total_counter == 3)

        # non-decorated update, confirm no increment and stale data in cache
        update_drunkard("Moe's", "Homer")
        assert (drunkard_total_counter == 3)
        assert (decorated_get_drunkard("Moe's") == "Barney")

        # decorated update, confirm increment and fresh data
        decorated_update_drunkard(alt_est_name="Moe's", drunk_name="Larry")
        assert (decorated_get_drunkard("Moe's") == "Larry")

        # decorated update with queuing refresh, confirm added to queue
        cache_obj = KCKCache.get_instance()
        c = cache_obj.queue_refresh_count("drunkard-by-establishment/Moe's")
        decorated_update_drunkard__queued_refresh(alt_est_name="Moe's", drunk_name="Carl")

        # assert that cache get returns the non-updated value
        assert (decorated_get_drunkard("Moe's") != "Carl")
        assert (cache_obj.queue_refresh_count("drunkard-by-establishment/Moe's") > c)

    def test_that_refresh_queue_param_works(self):
        """

        """

    def test_that_its_really_faster(self):
        """
        test that the kckrefresh decorator refreshes the cache entry as expected
        """

        global drunkard_total_counter

        # confirm counter is at zero
        assert (drunkard_total_counter == 0)

        NUMROWS = 1000

        # add some drunks to some bars
        for i, _ in enumerate(itertools.repeat(0, NUMROWS)):
            print("i: {}".format(i))
            decorated_add_drunkard(
                alt_est_name="bar{}".format(i), drunk_name="dude{}".format(i))
        assert (drunkard_total_counter == NUMROWS)

        # figure out how long it takes to find 1000 drunks without caching
        no_caching_time_start = datetime.datetime.now()
        for i in itertools.repeat(0, NUMROWS):
            get_drunkard("bar{}".format(randint(0, int(NUMROWS - 1))))
        no_caching_time_end = datetime.datetime.now()

        # figure out how long it takes to find 1000 drunks with caching
        caching_time_start = datetime.datetime.now()
        for i in itertools.repeat(0, NUMROWS):
            decorated_get_drunkard("bar{}".format(
                randint(0, int(NUMROWS - 1))))
        caching_time_end = datetime.datetime.now()

        # figure out how long each took
        delta_with_caching_for_all_rows = (
            caching_time_end - caching_time_start).seconds

        delta_without_caching_for_all_rows = (
            no_caching_time_end - no_caching_time_start).seconds
        delta_with_caching_for_one_row = delta_with_caching_for_all_rows / NUMROWS
        delta_without_caching_for_one_row = delta_without_caching_for_all_rows / NUMROWS

        # do the math, 10, 100, 1k, 10k
        for num_hits in [10, 100, 1000, 10000]:

            # assume queries that take 10, 100, 1k ms
            for query_time_in_ms in [10, 100, 1000]:

                # figure out how long it's likely to take for cache vs non-cache
                total_exec_without_caching_in_ms = (
                    query_time_in_ms * num_hits)
                total_exec_with_caching_in_ms = num_hits * delta_with_caching_for_one_row

                # assert that it's 100x faster for any query with exec time gte 10ms
                if query_time_in_ms >= 10:
                    assert (total_exec_with_caching_in_ms * 100 <
                            total_exec_without_caching_in_ms)

                # a little reporting
                print(
                    "without caching: {} gets for a task that takes {}ms takes {} seconds, "
                    + "but with caching, it'll take only {} seconds".format(
                        num_hits, query_time_in_ms, num_hits * query_time_in_ms
                        / 1000, total_exec_with_caching_in_ms / 1000 +
                        query_time_in_ms))

