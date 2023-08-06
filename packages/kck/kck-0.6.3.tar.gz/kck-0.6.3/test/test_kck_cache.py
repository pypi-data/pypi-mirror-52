import datetime
import os
import pytest
import json

from simple_settings import settings
from kck.lib.cassandra_actor import CassandraActor
from kck.lib.exceptions import KCKUnknownKey
from kck.lib.hints import HintsManager
from kck.lib.kck_cache import KCKCache, KCKKeyNotSetException

from kck.test.test_case import BaseBlankCassandraTestCase, BaseEnvironmentCheckingTestCase, BaseKCKTestCase

SCRIPT_DIRPATH = os.path.dirname(os.path.realpath(__file__))
KCK_SOURCES_DIRPATH = os.path.join(SCRIPT_DIRPATH, "..")


class TestKCKCacheRawMethods(BaseKCKTestCase, BaseBlankCassandraTestCase, BaseEnvironmentCheckingTestCase):

    def setup_method(self, method):
        self.setup_cassandra()

    def test__raw_cache_getput__basic(self):
        """test basic operation of raw_cache_get() and raw_cache_put()"""
        # init cache obj
        cache_obj = KCKCache(
            inhibit_framework_registration=True,
            compress=False,
            serialize=False
        )

        tbl = settings.KCK['cassandra']['tables']['primary_cache']

        # gen new version
        genver = cache_obj.gen_new_version()

        # assert that, because the key does not exist, _cache_get(key, tbl) will return no data
        res1 = cache_obj.raw_cache_get("key1", tbl)
        rows = 0
        for row in res1:
            rows += 1
        assert(rows <= 0)

        # put some data in there, assert that upserting doesn't return data
        res2 = cache_obj.raw_cache_put("key1", tbl, "val1".encode("utf-8"), version=genver)
        for row in res2:
            rows += 1
        assert(rows <= 0)

        # assert that there should be some data in there now
        res3 = cache_obj.raw_cache_get("key1", tbl)
        for row in res3:
            rows += 1
        assert (rows <= 1)

        # assert that we know what the data is
        res4 = cache_obj.raw_cache_get("key1", tbl)
        for row in res4:
            assert(row[0].decode() == "val1")
            assert(row[1] == genver)


    def test__raw_cache_delete(self):
        """test basic operation of raw_cache_delete()"""

        # init cache obj
        cache_obj = KCKCache(inhibit_framework_registration=True)
        tbl = settings.KCK['cassandra']['tables']['primary_cache']

        # gen new version
        genver = cache_obj.gen_new_version()

        # put some data in there
        res1 = cache_obj.raw_cache_put("key1", tbl, "val1".encode("utf-8"), version=genver)

        # assert that there should be some data in there now
        res2 = cache_obj.raw_cache_get("key1", tbl)
        rows = 0
        for row in res2:
            rows += 1
        assert (rows <= 1)

        # delete the key
        cache_obj.raw_cache_delete("key1", tbl)

        # assert that there should be no data in there now
        res3 = cache_obj.raw_cache_get("key1", tbl)
        rows = 0
        for row in res3:
            rows += 1
        assert (rows <= 0)

    def test__raw_cache_getput__version(self):
        """test that raw_cache_put() respects versions"""

        # init cache obj
        cache_obj = KCKCache(inhibit_framework_registration=True)
        tbl = settings.KCK['cassandra']['tables']['primary_cache']

        # gen new versions
        genver1 = cache_obj.gen_new_version()
        genver2 = cache_obj.gen_new_version()
        genver3 = cache_obj.gen_new_version()
        while True:
            if genver1 != genver2:
                break
            genver2 = cache_obj.gen_new_version()
        while True:
            if genver3 != genver2 and genver3 != genver1:
                break
            genver3 = cache_obj.gen_new_version()

        # put some data in there
        cache_obj.raw_cache_put("key1", tbl, "val1".encode("utf-8"), version=genver1)

        # assert that there should be some data in there now
        res1 = cache_obj.raw_cache_get("key1", tbl)
        for row in res1:
            assert (row[0].decode() == "val1")
            assert (row[1] == genver1)

        # try to put data in there with the wrong version number
        res2 = cache_obj.raw_cache_put("key1", tbl, "val2".encode("utf-8"), version=genver2, check_last_version=genver2)
        for row in res2:
            assert(row[0] == False)
        print("res2: {}, {}".format(res2, res2.__dict__))

        # assert that the data should be old
        res3 = cache_obj.raw_cache_get("key1", tbl)
        for row in res3:
            assert (row[0].decode() == "val1")
            assert (row[1] == genver1)

        # try to put data in there with the wrong version number
        res4 = cache_obj.raw_cache_put("key1", tbl, "val3".encode("utf-8"), version=genver3, check_last_version=genver1)
        for row in res4:
            assert(row[0] == True)
        print("res4: {}, {}".format(res4, res4.__dict__))

        # assert that the data should be old
        res5 = cache_obj.raw_cache_get("key1", tbl)
        for row in res5:
            assert (row[0].decode() == "val3")
            assert (row[1] == genver3)


class TestKCKCache(BaseKCKTestCase, BaseBlankCassandraTestCase, BaseEnvironmentCheckingTestCase):

    def setup_method(self, method):
        self.setup_cassandra()

    def test__cache_creates_keyspace(self):
        """test that instantiation of a KCKCache object creates the kck keyspace"""
        assert(not self.cassandra_keyspace_exists(settings.KCK['cassandra']['keyspace']))
        KCKCache(inhibit_framework_registration=True)
        assert (self.cassandra_keyspace_exists(settings.KCK['cassandra']['keyspace']))

    def test__cache_create_tables(self):
        """test that instantiation of a KCKCache object creates the cache tables"""
        tbl_primary_cache = settings.KCK['cassandra']['tables']['primary_cache']
        tbl_secondary_cache = settings.KCK['cassandra']['tables']['secondary_cache']

        # check that the primary and secondary cache tables do not exist
        assert (not self.cassandra_table_exists(tbl_primary_cache))
        assert (not self.cassandra_table_exists(tbl_secondary_cache))

        # init cache obj
        KCKCache(inhibit_framework_registration=True)

        # check that the primary and secondary cache tables exist
        assert (self.cassandra_table_exists(tbl_primary_cache))
        assert (self.cassandra_table_exists(tbl_secondary_cache))

    def test__cache_getput_basic(self):
        """test basic operation of _cache_get() and _cache_put()"""
        # init cache obj
        cache_obj = KCKCache(
            inhibit_framework_registration=True,
            compress=False,
            serialize=False
        )

        # test that key: 'key1' does not exist
        tbl = settings.KCK['cassandra']['tables']['primary_cache']
        with pytest.raises(KCKKeyNotSetException):
            cache_obj._cache_get("key1", tbl)

        # call _cache_put() and assert that the response is as expected
        res2 = cache_obj._cache_put("key1", tbl, "val1".encode("utf-8"))
        assert(res2["key"] == "key1")
        assert(res2["value"].decode() == "val1")
        assert(res2["success"] == True)
        assert(res2["version"] is not None)
        assert(res2["tbl"] == tbl)

        # test that key: 'key1' does exist and that the record returned
        # by _cache_get() is as expected
        res3 = cache_obj._cache_get("key1", tbl)
        assert(res3["value"].decode() == "val1")
        assert(res3["version"] == res2["version"])
        assert(res3["key"] == "key1")
        assert(res3["tbl"] == tbl)

    def test__cache_delete(self):
        """test basic operation of _cache_delete()"""
        # init cache obj
        cache_obj = KCKCache(
            inhibit_framework_registration=True,
            compress=False,
            serialize=False
        )

        # test that key: 'key1' does not exist
        tbl = settings.KCK['cassandra']['tables']['primary_cache']
        with pytest.raises(KCKKeyNotSetException):
            cache_obj._cache_get("key1", tbl)

        # call _cache_put()
        res2 = cache_obj._cache_put("key1", tbl, "val1".encode("utf-8"))

        # test that key now exists
        res3 = cache_obj._cache_get("key1", tbl)
        assert(res3["value"].decode() == "val1")
        assert(res3['success'])

        # delete the key
        cache_obj._cache_delete("key1", tbl)

        # test that key no longer exists
        with pytest.raises(KCKKeyNotSetException):
            cache_obj._cache_get("key1", tbl)

    def test_refresh_with_queued_flag_adds_to_refresh_queue(self):

        def get_queue_contents():

            # get queue names from config
            refresh_queue_name = settings.KCK['cassandra']['tables']['queued_refreshes']
            refresh_counter_name = settings.KCK['cassandra']['tables']['queued_refreshes_counter']

            # async refresh queue query
            q_hints = "select kck_key, kck_hints from {}".format(refresh_queue_name)
            pq_hints = cache_obj.session.prepare(q_hints)
            fut_hints = cache_obj.session.execute_async(pq_hints)

            # async refresh counters query
            q_counts = "select kck_key_version, refresh_request_counter from {}".format(
                refresh_counter_name
            )
            pq_counts = cache_obj.session.prepare(q_counts)
            fut_result = cache_obj.session.execute(pq_counts)

            queue_dict = {}
            for key_hints_tuple in fut_hints.result():
                key, hints = key_hints_tuple
                queue_dict[key] = {"raw_hints": json.loads(hints)}

            for key_count_tuple in fut_result:
                key_version, cnt = key_count_tuple
                key_version_tuple = key_version.split(CassandraActor.key_ver_sep)
                key, version = key_version_tuple
                queue_dict[key]["refresh_request_counter"] = cnt

            return queue_dict

        # init cache obj
        cache_obj = KCKCache()

        queue_count_dict_pre = get_queue_contents()
        assert(not(bool(queue_count_dict_pre)))
        hints = HintsManager(cache_obj)
        print("hints dump1: {}".format(hints.to_dict()))
        hints.set_hint_key(
            cache_obj.build_cache_entry_dict(
                key='simple_expiry/1',
                version=1,
                value='justastring',
                tbl='some_cache_table',
                modified=datetime.datetime.utcnow()))
        print("hints dump2: {}".format(hints.to_dict()))
        cache_obj.refresh("simple1/1", hints=hints, queued=True)

        queue_count_dict_post = get_queue_contents()
        assert(bool(queue_count_dict_post))
        assert('simple1/1' in queue_count_dict_post)
        queue_entry = queue_count_dict_post["simple1/1"]
        print('qe: {}'.format(queue_entry))
        assert(queue_entry["refresh_request_counter"] == 1)
        assert(len(queue_entry['raw_hints']['hints'].keys()) == 1)

    def test_cache_set_supersedes_primer_registration(self):
        """test that KCKCache can be used as a general-purpose cache
        and keys can be set and returned regardless of whether or not
         a primer exists"""
        cache_obj = KCKCache(inhibit_framework_registration=True)
        with pytest.raises(KCKUnknownKey):
            cache_obj.get("somekey/1")
        cache_obj.set("somekey/1", 1)

        cache_result = cache_obj.get("somekey/1")
        assert(bool(cache_result["success"]))
        assert(cache_result["value"] == 1)

    def test_cache_set_updates_primary_and_secondary_caches(self):

        # test that cache_get raises exception for keys
        key = 'test_cache_set_updates_primary_and_secondary_caches__some_key'
        cache_obj = KCKCache(inhibit_framework_registration=True)
        with pytest.raises(KCKKeyNotSetException):
            cache_obj._primcache_get(key)
        with pytest.raises(KCKKeyNotSetException):
            cache_obj._seccache_get(key)

        # call set
        cache_obj.set(key, 'someval')

        # test that cache_get returns values
        assert(cache_obj._primcache_get(key), 'someval')
        assert(cache_obj._seccache_get(key), 'someval')

    def test_mget_returns_multiple_results(self):
        cache_obj = KCKCache(inhibit_framework_registration=True)
        cache_obj.set('k1', 'v1')
        cache_obj.set('k2', 'v2')
        cache_obj.set('k3', 'v3')
        assert([res['value'] for res in cache_obj.mget(['k1', 'k2', 'k3'])] == ['v1', 'v2', 'v3'])

    def test_mget_returns_exceptions(self):
        cache_obj = KCKCache(inhibit_framework_registration=True)
        cache_obj.set('k11', 'v1')
        cache_obj.set('k31', 'v3')
        mget_result = cache_obj.mget(['k11', 'k21', 'k31'])
        assert ([res.get('value') for res in mget_result] == ['v1', None, 'v3'])
        assert (type(mget_result[1]['exception']) == KCKUnknownKey)

