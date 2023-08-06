import time
import json
import logging
from tornado.testing import AsyncHTTPTestCase
from kck.lib.http_service import KCKHTTPServer
from kck.lib.kck_cache import KCKCache
from kck.lib.kck_database import KCKDatabase
from kck.test.test_case import (BaseBlankCassandraTestCase,
                                BaseEnvironmentCheckingTestCase,
                                BasePostgresqlSeedingTestCase, BaseKCKTestCase)

logger = logging.getLogger(__name__)


class TestDependentRefresh(BaseKCKTestCase, AsyncHTTPTestCase, BaseBlankCassandraTestCase,
                           BaseEnvironmentCheckingTestCase,
                           BasePostgresqlSeedingTestCase):
    def get_app(self):
        return KCKHTTPServer.get_instance()

    def setup_method(self, method):
        self.setup_cassandra()
        self.setup_postgresql()

    def assert_successful_fetch(self, cache_obj, key, value):
        r = cache_obj.get(key, prime_on_cache_miss=True)
        assert (r['success'])
        assert (r['key'] == key)
        logger.debug('key: {}, pval: {}, tval: {}'.format(key, value, r['value'][0][0]))
        assert (r['value'][0][0] == value)

    def test_refresh_after_prime(self):

        # build some tables for caching in cassandra
        cache_obj = KCKCache.get_instance(
            refresh_selector_string="test_refresh_worker", new_instance=True)

        self.assert_successful_fetch(cache_obj, 'simple_refresh_on_prime1/1', 'homer')

        # change the record and assert that the key remains what it
        #  was before the change
        print("\nchanging value to marge in database...")
        KCKDatabase.query("test", """
                update testtbl1
                set testcol1 = 'marge'
                where id = 1
            """)
        self.assert_successful_fetch(cache_obj, 'simple_refresh_on_prime1/1',
                                     'homer')

        # fetch the simple1 key to trigger the refresh of simple_refresh_on_prime1
        self.assert_successful_fetch(cache_obj, 'simple1/1', 'marge')

        cache_obj.perform_queued_refreshes()

        # fetch the simple_refresh_on_prime1 record and assert that it
        # now matches the new record
        self.assert_successful_fetch(cache_obj, 'simple_refresh_on_prime1/1',
                                     'marge')

        # assert(False)

    def test_refresh_after_update(self):
        """
        test:
          1) key/val is what's expected (homer)
          2) call update with new data (bart),
          3) confirm that key/val has updated.
        """

        # test that the key/val is as expected
        cache_obj = KCKCache.get_instance(
            refresh_selector_string="test_refresh_worker",
            new_instance=True)
        self.assert_successful_fetch(
            cache_obj,
            'simple_refresh_on_update1/1',
            'homer')

        # update and perform queued refresh
        cache_obj.data_obj.update('simple_updater1/1', {"id": 1, "testcol1": "bart"})

        qryres = list(KCKDatabase.query('test', 'select testcol1 from testtbl1 where id = :id', {'id': 1}))
        assert qryres[0]['testcol1'] == 'bart'

        cache_obj.perform_queued_refreshes()

        sleep_seconds = 0.1
        total_seconds_slept = 0
        while True:
            assert(total_seconds_slept < 8)
            try:
                self.assert_successful_fetch(
                    cache_obj, 'simple_refresh_on_update1/1', 'bart'
                )
                break
            except AssertionError:
                time.sleep(sleep_seconds)
                total_seconds_slept += sleep_seconds
                sleep_seconds *= 1.1

