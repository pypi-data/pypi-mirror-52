import datetime

from kck.lib.hints import HintsManager
from .log import log
import logging
from .cassandra_actor import CassandraActor

process_data_singleton = None
logger = logging.getLogger(__name__)


class KCKData(CassandraActor):

    _pcol = None
    parameters = None
    cache_obj = None

    @classmethod
    def get_instance(cls, **kwargs):
        global process_data_singleton
        if process_data_singleton is None:
            process_data_singleton = cls(**kwargs)
        return process_data_singleton

    def __init__(self, inhibit_framework_registration=False, cache_obj=None):
        self.primitive_init()
        if cache_obj is None:
            from kck.lib.kck_cache import KCKCache
            self.init(
                inhibit_framework_registration=inhibit_framework_registration,
                cache_obj=KCKCache.get_instance(data_obj=self),
                data_obj=self)
        else:
            self.init(
                inhibit_framework_registration=inhibit_framework_registration,
                cache_obj=cache_obj,
                data_obj=self)

    def register_updater(self, name, updater_obj):
        updater_obj.set_data(self)
        updater_obj.set_cache(self.cache_obj)
        updater_obj.set_name(name)
        self.updaters[name] = updater_obj

    def updater(self, name):
        return self.updaters[name]

    def update(self, keystr, data):
        logger.info('update - key: {}, data: {}'.format(keystr, data))
        u = self._updater_obj(keystr)
        hints = HintsManager(self.cache_obj)
        u.do_hooks("pre_update", key=keystr, hints=hints)
        r = u.update(data)

        u.do_hooks("post_update", key=keystr, hints=hints)
        return dict(success=True)

    def _updater_obj(self, key):
        ret = self.updater(key.split(self.keysep)[0])
        return ret
