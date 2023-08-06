from kck.lib.kck_database import KCKDatabase
from kck.test.test_case import (BasePostgresqlSeedingTestCase,
                                BaseBlankCassandraTestCase,
                                BaseEnvironmentCheckingTestCase,
                                BaseCacheInitTestCase, BaseKCKTestCase)


class TestRefreshOverDomain(BaseKCKTestCase,
                            BasePostgresqlSeedingTestCase,
                            BaseBlankCassandraTestCase,
                            BaseEnvironmentCheckingTestCase,
                            BaseCacheInitTestCase):

    def setup_method(self, method):
        self.setup_cassandra()
        self.setup_postgresql()
        self.setup_cache()

    def test_refresh_over_domain(self):

        # seed test data to db
        people_map1 = {
            10: "homer",
            20: "marge",
            30: "bart",
            40: "lisa",
            50: "maggie"}
        for id, person_name in people_map1.items():
            KCKDatabase.query(
                "test",
                """
                    insert into testtbl1
                    (id, testcol1)
                    VALUES
                    ({}, '{}')
                """.format(id, person_name))


