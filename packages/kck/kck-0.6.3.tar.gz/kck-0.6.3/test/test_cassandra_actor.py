import pytest

from kck.lib.cassandra_actor import PerformQueuedRefreshesRequiresRefreshSelectorException
from kck.lib.exceptions import KCKKeyNotSetException
from kck.lib.kck_cache import KCKCache
from kck.test.test_case import (
    BaseBlankCassandraTestCase, BasePostgresqlSeedingTestCase, BaseRefreshQueueTestCase,
    BaseCacheInitTestCase, BaseKCKTestCase)


class TestCassandraActorQueuesRefreshRequests(BaseKCKTestCase,
                                              BaseBlankCassandraTestCase,
                                              BasePostgresqlSeedingTestCase,
                                              BaseCacheInitTestCase):

    def setup_method(self, method):
        self.setup_cassandra()
        self.setup_postgresql()
        self.setup_cache()

    def test_count(self):

        # get the count for simple/1
        # cache_obj = KCKCache.get_instance()
        c = self.cache_obj.queue_refresh_count("simple1/1")

        # queue a refresh request
        self.cache_obj.refresh("simple1/1", queued=True)

        # show that the count incremented
        assert(self.cache_obj.queue_refresh_count("simple1/1") > c)


class TestCassandraActorPerformQueuedRefreshes(BaseKCKTestCase,
                                               BaseBlankCassandraTestCase,
                                               BasePostgresqlSeedingTestCase,
                                               BaseRefreshQueueTestCase):

    def setup_method(self, method):
        self.setup_cassandra()
        self.setup_postgresql()
        self.setup_refresh_queue_test()
        KCKCache.get_instance(new_instance=True, refresh_selector_string="test_refresh_worker")

    def test_perform_queued_refreshes_without_selector_raises_exception(self):
        cache_obj = KCKCache()
        with pytest.raises(PerformQueuedRefreshesRequiresRefreshSelectorException):
            cache_obj.perform_queued_refreshes()

    def test_refresh_single(self):

        # queue a refresh request
        self.cache_obj.refresh("simple1/1", queued=True)

        # it should raise a KCKKeyNotSetException because simple1/1
        # has not been primed
        with pytest.raises(KCKKeyNotSetException):
            cache_entry_rec = self.cache_obj.get("simple1/1")

        # perform queued refreshes (incl. simple1/1)
        self.cache_obj.perform_queued_refreshes()

        # get simple1/1 cache entry and confirm it is as expected
        cache_entry_rec = self.cache_obj.get("simple1/1")
        assert(cache_entry_rec['success'])
        assert(cache_entry_rec['value'][0][0] == 'homer')

    def test_partial_claim_success(self):

        # queue some refresh requests
        self.cache_obj.refresh("simple1/1", queued=True)
        self.cache_obj.refresh("simple1/2", queued=True)
        self.cache_obj.refresh("simple1/3", queued=True)

        # get the queue data to be used by claim_refresh_requests
        refresh_data = self.cache_obj.queued_refresh_data(limit=3)

        # update the selector, simulating a competing claim
        self.update_selector_on_refresh_queue_entry("simple1/2", "claimed_by_other_process")

        # attempt to claim all the refresh requests in refresh data
        async_claim_requests = self.cache_obj.claim_refresh_requests(refresh_data)

        # assemble results
        claim_request_result_list = []
        for key_fut_tuple in async_claim_requests:
            key, fut = key_fut_tuple
            result = fut.result()
            if result[0][0]:
                claim_request_result_list.append(key)

        # show that simple1/2 was unclaimable
        assert('simple1/1' in claim_request_result_list)
        assert('simple1/2' not in claim_request_result_list)
        assert('simple1/3' in claim_request_result_list)

        # show that a second call to queued_refresh_data returns
        # an empty dict as expected
        refresh_data2 = self.cache_obj.queued_refresh_data(limit=3)

        assert(not refresh_data2)