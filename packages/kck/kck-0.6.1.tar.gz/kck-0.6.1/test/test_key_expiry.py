import pytest

import time
from kck.lib.exceptions import KCKKeyNotSetException
from kck.lib.kck_cache import KCKCache
from kck.test.test_case import BaseBlankCassandraTestCase, BasePostgresqlSeedingTestCase, BaseKCKTestCase


class TestKeyExpiry(BaseKCKTestCase, BasePostgresqlSeedingTestCase, BaseBlankCassandraTestCase):
    def setup_method(self, method):
        self.setup_cassandra()
        self.setup_postgresql()

    def test_yaml_expiry(self):
        """Test that the expiry is being respected for YAML primers"""

        def assert_successful_fetch(cache_obj, key, value):
            r = cache_obj.get(key)
            assert (r['success'])
            assert (r['key'] == key)
            assert (r['value'][0][0] == value)

        # refresh key
        cache_obj = KCKCache()
        print("cp0")
        cache_obj.refresh('simple_expiry1/1')
        print("cp10")
        # verify that the cache entry is as expected
        assert_successful_fetch(cache_obj, 'simple_expiry1/1', 'homer')
        print("cp20")
        # sleep past expiry
        time.sleep(1.1)
        print("cp30")
        # test that the entry is no longer set
        with pytest.raises(KCKKeyNotSetException) as e_info:
            assert_successful_fetch(cache_obj, 'simple_expiry1/1', 'marge')
