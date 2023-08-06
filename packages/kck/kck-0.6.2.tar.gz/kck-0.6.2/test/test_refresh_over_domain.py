import json

import time
from tornado.testing import AsyncHTTPTestCase

# from kck.lib.config import kck_config_lookup
from kck.lib.http_service import KCKHTTPServer
from kck.lib.kck_cache import KCKCache
from kck.lib.kck_database import KCKDatabase
from kck.test.test_case import (BasePostgresqlSeedingTestCase,
                                BaseBlankCassandraTestCase,
                                BaseEnvironmentCheckingTestCase,
                                BaseCacheInitTestCase)


class TestRefreshOverDomain(BasePostgresqlSeedingTestCase,
                            BaseBlankCassandraTestCase,
                            BaseEnvironmentCheckingTestCase,
                            BaseCacheInitTestCase):

    def setup_method(self):
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

        # refresh and fetch domain ids
        self.cache_obj.refresh("refresh_over_domain_ids")
        domain_ids = self.cache_obj.get("refresh_over_domain_ids")

        print("domain ids: {domain_ids}".format(domain_ids=domain_ids))

        # call do_processes() to request refreshes and perform_queued_refreshes()
        # to perform them
        self.cache_obj.do_processes()
        self.cache_obj.perform_queued_refreshes()

        # update the names in the database (not the cache)
        people_map2 = {
            10: "ned",
            20: "barney",
            30: "moe",
            40: "edna",
            50: "montgomery"}
        for id, person_name in people_map2.items():
            KCKDatabase.query(
                "test",
                """
                    update testtbl1
                    set testcol1='{}'
                    where id={}
                """.format(person_name, id))

        # test that the cache values reflect the original seeded values, not the updated values
        # (proving that the entirety of the domain was cached)
        for id, person_name in people_map1.items():
            assert(self.cache_obj.get("refresh_over_domain1/{}".format(id))["value"] == person_name)

