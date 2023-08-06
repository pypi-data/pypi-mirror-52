from kck.lib import KCKCache
from kck.test.test_case import (BaseBlankCassandraTestCase,
                                BaseEnvironmentCheckingTestCase,
                                BasePostgresqlSeedingTestCase, BaseCacheInitTestCase, BaseKCKTestCase)

class TestAugmentingPrimerClasses(BaseKCKTestCase,
                                  BaseBlankCassandraTestCase,
                                  BaseEnvironmentCheckingTestCase,
                                  BasePostgresqlSeedingTestCase,
                                  BaseCacheInitTestCase):
    def setup_method(self, method):
        self.setup_postgresql()
        self.setup_cassandra()
        self.setup_cache()

    def _unordered_equal(self, result_rows_1, result_rows_2):
        if len(result_rows_1) != len(result_rows_2):
            return False
        eq_count = 0
        for r in result_rows_1:
            for rr in result_rows_2:
                if list(r) == list(rr):
                    eq_count += 1
        return eq_count == len(result_rows_1)

    def _assert_unordered_equal(self, result_rows_1, result_rows_2):
        assert (self._unordered_equal(result_rows_1, result_rows_2))

    def _assert_unordered_not_equal(self, result_rows_1, result_rows_2):
        assert (not self._unordered_equal(result_rows_1, result_rows_2))

    def _row_in_rows(self, row, rows):
        for r in rows:
            if list(r) == list(row):
                return True
        return False

    def _assert_row_in_rows(self, row, rows):
        assert(self._row_in_rows(row, rows))

    def _assert_row_not_in_rows(self, row, rows):
        assert (not self._row_in_rows(row, rows))

    def test_trigger_set_augments_target(self):
        """test that the augmentation occurs when perform_queued_updates is called"""

        # refresh the primer target
        self.cache_obj.refresh('simpleaugmentingprimertarget')

        # current val
        target_val_1 = self.cache_obj.get('simpleaugmentingprimertarget')
        assert(target_val_1['success'])

        # set constituent data
        self.cache_obj.set('simpleaugmentingprimertrigger/1', 'ned')

        # check val is the same before calling perform_queued_refreshes()
        target_val_2 = self.cache_obj.get('simpleaugmentingprimertarget')
        self._assert_unordered_equal(target_val_1['value'], target_val_2['value'])

        # do refreshes
        self.cache_obj.perform_queued_refreshes()

        # check that target val has been updated
        target_val_3 = self.cache_obj.get('simpleaugmentingprimertarget')
        self._assert_unordered_not_equal(target_val_1['value'], target_val_3['value'])
        self._assert_row_not_in_rows([1,"ned"], target_val_1['value'])
        self._assert_row_in_rows([1,"ned"], target_val_3['value'])


class TestAugmentingDecorators(BaseKCKTestCase,
                               BaseBlankCassandraTestCase,
                               BaseEnvironmentCheckingTestCase,
                               BasePostgresqlSeedingTestCase):

    def setup_method(self):
        self.setup_postgresql()
        self.setup_cassandra()
        self.cache_obj = KCKCache.get_instance(new_instance=True)

