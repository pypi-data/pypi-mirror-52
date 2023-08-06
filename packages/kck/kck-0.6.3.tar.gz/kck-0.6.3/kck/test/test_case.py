import json
import time
from unittest import TestCase

from simple_settings import settings
# from kck.lib.config import kck_config_lookup, kck_environment, kck_config_filepath
from kck.lib.kck_auth import use_auth
from kck.lib.kck_cache import KCKCache
from kck.lib.kck_database import KCKDatabase
from kck.test.cache import SimpleTestCache
from cassandra.cluster import Cluster


class BaseKCKTestCase(TestCase):
    pass


class BasePostgresqlSeedingTestCase(object):

    def setup_postgresql(self):
        self._delete_postgres_tables()
        self._create_postgres_tables()
        self._seed_postgres_tables()

    def _delete_postgres_tables(self):
        KCKDatabase.query("test", "drop table if exists testtbl1")
        KCKDatabase.query("test", "drop table if exists testtbl2")

    def _create_postgres_tables(self):
        KCKDatabase.query(
            "test",
            """
                create table testtbl1 (
                    id integer,
                    testcol1 varchar(256)
                )
            """
        )
        KCKDatabase.query(
            "test",
            """
                create table testtbl2 (
                    id integer,
                    testcol2 varchar(256)
                )
            """
        )

    def _seed_postgres_tables(self):
        for ndx, name in enumerate(['homer', 'barney', 'carl', 'lenny']):
            KCKDatabase.query(
                "test",
                """
                    insert into testtbl1
                    (id, testcol1)
                    VALUES
                    (:ndx, :name)
                """,
                dict(ndx=ndx+1, name=name)
            )
        KCKDatabase.query(
            "test",
            """
                insert into testtbl2
                (id, testcol2)
                VALUES
                (1, 'marge')
            """
        )


class BaseTestCacheTestCase(object):
    cache_obj = None

    def setup_test_cache(self):
        self.cache_obj = SimpleTestCache()


class BaseCassandraTestCase(object):

    def cassandra_table_exists(self, tbl):
        session = Cluster(settings.KCK['cassandra']['hosts']).connect()
        return bool(
            session.execute(
                "SELECT * FROM system_schema.tables " +
                "WHERE keyspace_name='{}' and table_name='{}'".format(
                    settings.KCK['cassandra']['keyspace'],
                    tbl)))

    def cassandra_keyspace_exists(self, ks):
        session = Cluster(settings.KCK['cassandra']['hosts']).connect()
        return bool(
            session.execute(
                "SELECT * FROM system_schema.keyspaces WHERE keyspace_name='{}'".format(ks)))


class BaseBlankCassandraTestCase(BaseCassandraTestCase):

    def setup_cassandra(self):
        self._delete_cassandra_tables()
        time.sleep(0.3)
        session2 = Cluster(settings.KCK['cassandra']['hosts']).connect()
        session2.execute("DROP KEYSPACE IF EXISTS {}".format(
            settings.KCK['cassandra']['keyspace']))

    def _delete_cassandra_table(self, cache_obj, tbl):
        cache_obj.session.execute("DROP TABLE IF EXISTS {}".format(tbl))

    def _delete_cassandra_tables(self):
        cache_obj1 = KCKCache.get_instance(inhibit_framework_registration=True)
        for _, tbl in settings.KCK['cassandra']['tables'].items():
            self._delete_cassandra_table(cache_obj1, tbl)


class BaseEnvironmentCheckingTestCase(object):
    @classmethod
    def setup_class(cls):
        environment = settings.KCK['environment']
        if environment != "test":
            raise (Exception("KCK_ENVIRONMENT != 'test'...aborting"))
        use_auth(reset=True)


class BaseHTTPServerTestCase(object):

    def assert_response_is_valid(self, response):
        assert (response.code == 200)
        assert (response.body is not None)
        response_data = json.loads(str(response.body, 'utf-8'))
        assert ('success' in response_data)

    def assert_response_is_error(self, response, **kwargs):
        self.assert_response_is_valid(response)
        response_data = json.loads(str(response.body, 'utf-8'))
        assert ('error' in response_data)
        assert (not bool(response_data['success']))
        error_data = response_data['error']
        assert ('name' in error_data)
        assert ('args' in error_data)
        
        if 'name' in kwargs:
            assert (error_data['name'] == kwargs['name'])

        if 'args' in kwargs:
            assert(error_data['args'] == kwargs['args'])

    def assert_response_success(self, response, **kwargs):
        self.assert_response_is_valid(response)
        response_data = json.loads(str(response.body, 'utf-8'))

        assert(bool(response_data['success']))

        for arg, val in kwargs.items():
            assert(arg in response_data)
            assert(response_data[arg] == val)


class BaseCacheInitTestCase(object):
    def setup_cache(self):
        self.cache_obj = KCKCache.get_instance(new_instance=True,
                                               refresh_selector_string="test_refresh_worker")
        self.cache_obj.refresh('refreshingclassbased2/1')


class BaseRefreshQueueTestCase(BaseCacheInitTestCase):
    def setup_refresh_queue_test(self):
        self.setup_cache()

    def update_selector_on_refresh_queue_entry(self, key, selector):
        pq = self.cache_obj.session.prepare(
            """

            update {} set selector = ? where kck_key = ?

            """.format(self.cache_obj.refresh_queue_name)
        )
        self.cache_obj.session.execute(pq, (selector, key))
