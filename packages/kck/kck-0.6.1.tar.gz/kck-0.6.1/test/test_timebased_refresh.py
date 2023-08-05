import time

from kck.lib.kck_database import KCKDatabase
from kck.test.test_case import (BaseBlankCassandraTestCase,
                                BasePostgresqlSeedingTestCase,
                                BaseEnvironmentCheckingTestCase,
                                BaseCacheInitTestCase, BaseKCKTestCase)


class TestTimeBasedRefresh(BaseKCKTestCase, BaseBlankCassandraTestCase,
                           BasePostgresqlSeedingTestCase,
                           BaseEnvironmentCheckingTestCase,
                           BaseCacheInitTestCase):
    def setup_method(self, method):
        self.setup_cassandra()
        self.setup_postgresql()
        self.setup_cache()

    def test_timebasedrefresh(self):

        self.cache_obj.refresh('refreshingclassbased2/1')
        cache_rec_orig = self.cache_obj.get('refreshingclassbased2/1')
        assert(cache_rec_orig['value'] == [['marge']])

        KCKDatabase.query(
            "test",
            """
                update testtbl2
                set testcol2 = 'lisa'
                where id = 1
            """
        )

        cache_rec_just_after = self.cache_obj.get('refreshingclassbased2/1')
        assert (cache_rec_just_after['value'] == [['marge']])

        time.sleep(2.1)
        self.cache_obj.do_processes()
        self.cache_obj.perform_queued_refreshes()

        cache_rec_just_after = self.cache_obj.get('refreshingclassbased2/1')
        assert (cache_rec_just_after['value'] == [['lisa']])

