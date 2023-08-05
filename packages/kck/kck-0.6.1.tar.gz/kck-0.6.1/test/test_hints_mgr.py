import copy
from unittest.mock import patch
from simple_settings import settings
import datetime
import pytest
from kck.lib.exceptions import KCKKeyNotSetException, KCKKeyNotRegistered

from kck.lib.kck_primer import KCKPrimer

from kck.lib import KCKCache
from kck.lib.hints import HintsManager
from kck.test.test_case import BaseBlankCassandraTestCase, BaseCacheInitTestCase, BaseKCKTestCase


class TestHintsManager(BaseKCKTestCase, BaseBlankCassandraTestCase, BaseCacheInitTestCase):
    def setup_method(self, method):
        self.setup_cassandra()
        self.setup_cache()
        self.hints_manager = HintsManager(self.cache_obj)

    def test_no_match_falls_through_to_cache(self):
        with patch('kck.lib.KCKCache.get') as mock_cache_get:

            # hints mgr is blank, so anything should go to cache get
            self.hints_manager.get('anything')

            assert(mock_cache_get.call_count > 0)

    def test_match_returns_hinted_cache_entry(self):

        params = dict(
            key='somekey',
            version='v1.catdog',
            value='somevalue',
            tbl='sometbl',
            modified=datetime.datetime.utcnow())

        cache_entry_input = KCKCache.build_cache_entry_dict(**params)
        expected_output = copy.copy(cache_entry_input)

        self.hints_manager.set_hint_key(cache_entry_input)

        with patch('kck.lib.KCKCache.get') as mock_cache_get:
            assert(self.hints_manager.get(cache_entry_input['key']) == expected_output)
            assert(mock_cache_get.call_count == 0)

    def test_purge_match_raises_notset_exception_when_primer_registered(self):
        class MinPrimer(KCKPrimer):
            pass
        some_primer_obj = MinPrimer()
        self.cache_obj.register_primer('somekey', some_primer_obj)
        self.hints_manager.unset_hint_key('somekey')
        with pytest.raises(KCKKeyNotSetException):
            self.hints_manager.get('somekey')

    def test_purge_match_raises_notregistered_when_primer_not_registered(self):
        tbl_dict = settings.KCK['cassandra']['tables']
        self.prim_cache_name = tbl_dict['primary_cache']
        r = self.hints_manager.get('somekey')
        print("r: {}".format(r))
