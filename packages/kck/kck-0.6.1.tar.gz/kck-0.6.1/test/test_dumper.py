import os
from kck.lib import KCKCache
from kck.test.test_case import BaseBlankCassandraTestCase, BaseKCKTestCase

DEFAULT_DUMP_FILEPATH = '/tmp/kck_dump.out'


class TestDumper(BaseKCKTestCase, BaseBlankCassandraTestCase):

    def setup_method(self, method):
        self.setup_cassandra()
        cache_obj = KCKCache.get_instance(inhibit_framework_registration=True, new_instance=True)
        cache_obj.set('val1', 'simple')
        cache_obj.set('val2', ['less', 'simple'])
        cache_obj.set('val3', {'desc': ['even', 'less', 'simple']})
        if os.path.exists(DEFAULT_DUMP_FILEPATH):
            os.unlink(DEFAULT_DUMP_FILEPATH)

    def assert_equal(self, a, b):
        assert a == b


    def test_data_dump_writes_file(self):

        # dump to file
        cache_obj = KCKCache.get_instance()
        cache_obj.dump_data_to_file()

        # assert file exists
        assert(os.path.exists(DEFAULT_DUMP_FILEPATH))

    def test_data_dump_recreates_cache(self):

        # dump to file
        cache_obj = KCKCache.get_instance()
        cache_obj.dump_data_to_file()

        # clear cassandra
        self.setup_cassandra()

        # re-init cache and load from file
        cache_obj = KCKCache.get_instance(inhibit_framework_registration=True, new_instance=True)
        cache_obj.load_data_from_file()

        # verify cache contents
        self.assert_equal(cache_obj.get('val1')['value'], 'simple')
        self.assert_equal(cache_obj.get('val2')['value'], ['less', 'simple'])
        self.assert_equal(cache_obj.get('val3')['value'], {'desc': ['even', 'less', 'simple']})