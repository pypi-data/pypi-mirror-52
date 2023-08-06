import json
import os
import random
import zlib
import pickle
import dateutil.parser
import datetime
import logging

from simple_settings import settings
# from .config import kck_config_lookup
from kck.lib.hints import HintsManager
from .exceptions import PrimerComputerReturnedNoResults, KCKKeyNotSetException, KCKKeyNotRegistered, KCKUnknownKey, \
    CanNotAugmentWithoutVersion, CantAugmentUnknownPrimer, VersionedRefreshMismatchException, \
    ComputeAugmentedValueNotImplemented
from .cassandra_actor import CassandraActor

SCRIPT_DIRPATH = os.path.dirname(os.path.realpath(__file__))
KCK_SOURCES_DIRPATH = os.path.join(SCRIPT_DIRPATH, "..")

process_cache_singleton = None
logger = logging.getLogger(__name__)


class KCKCache(CassandraActor):

    prime_on_cache_miss = False

    def __init__(self,
                 inhibit_framework_registration=False,
                 key_string_sep="/",
                 serialize=True,
                 compress=True,
                 data_obj=None,
                 refresh_selector_string=None):
        """

        :param inhibit_framework_registration:
        :param key_string_sep:
        :param serialize:
        :param compress:
        :param data_obj:

        :param refresh_selector_string:
            the value that is to be assigned to the selector field of refresh queue
            records when they are 'claimed' by the refresh worker

        """
        self.primitive_init()
        if data_obj is None:
            from .kck_data import KCKData
            self.init(
                inhibit_framework_registration=inhibit_framework_registration,
                cache_obj=self,
                data_obj=KCKData.get_instance(cache_obj=self),
                serialize=serialize,
                compress=compress)
        else:
            self.init(
                inhibit_framework_registration=inhibit_framework_registration,
                cache_obj=self,
                data_obj=data_obj,
                serialize=serialize,
                compress=compress)

        self.prime_on_cache_miss = settings.KCK['prime_on_cache_miss']
        self.keysep = key_string_sep

        self.refresh_selector_string = refresh_selector_string

    @classmethod
    def get_instance(cls, **kwargs):
        global process_cache_singleton
        if process_cache_singleton is None or "new_instance" in kwargs and kwargs["new_instance"]:
            if 'new_instance' in kwargs:
                kwargs.pop('new_instance')
            process_cache_singleton = cls(**kwargs)
        return process_cache_singleton

    @staticmethod
    def gen_new_version():
        """returns a new random integer to be used for versioning"""
        minver = -2147483648
        maxver = 2147483647
        return random.randint(minver, maxver)

    def mget(self, key_list, prime_on_cache_miss=False):
        ret = []
        for key in key_list:
            try:
                ret.append(self.get(key, prime_on_cache_miss=prime_on_cache_miss))
            except KCKUnknownKey as e:
                ret.append(
                    dict(
                        success=False,
                        key=key,
                        exception=e
                    )
                )
            except Exception as e:
                logger.debug("kck_cache.KCKCache.mget - shouldn't be getting here...need to add a handled exception")
                raise e
        return ret

    def set(self, key, val, expire=None, version=None):
        """places a cache entry in the primary cache with key=key and value=val"""
        self._primcache_put_and_set_hooks(key, val, expire=expire, version=version)
        self._seccache_put(key, val, expire=expire)

        # try to call any augment listeners
        # try:
        #     self._do_on_event_augment(key, 'update', value=val)
        # except CantAugmentUnknownPrimer:
        #     pass

    def get(self, key, prime_on_cache_miss=False):
        """given a key, try to find a corresponding value in the primary cache. failing that,
           try to find the corresponding value in the secondary cache. failing that, if
           self.prime_on_cache_miss is True, call the primer"""

        try:
            ret = self._primcache_get(key)
            return ret

        except KCKKeyNotSetException:

            try:
                self.primer_obj(key)
            except KCKKeyNotRegistered:

                try:
                    ret = self._seccache_get(key)
                    return ret
                except KCKKeyNotSetException:
                    raise KCKUnknownKey(key)

            # if kck is depending on the val cached in the
            # secondary cache, it's time to refresh
            # self.refresh(key, queued=True)

            if not self.prime_on_cache_miss and not prime_on_cache_miss:

                ret = self._seccache_get(key)
                self.refresh(key, queued=True)
                return ret

            try:
                ret = self._seccache_get(key)
                self.refresh(key, queued=True)
                return ret

            except KCKKeyNotSetException:
                try:
                    return self._prime(key)
                except PrimerComputerReturnedNoResults:
                    raise KCKKeyNotSetException(
                        key,
                        self.prim_cache_name,
                        msg="primer found, but compute() returned no results")

    def dump_data_to_file(self, output_filename='/tmp/kck_dump.out'):
        self.raw_cache_dump(tbl=self.sec_cache_name, output_filename=output_filename)

    def load_data_from_file(self, input_filename='/tmp/kck_dump.out'):
        self.raw_cache_load(tbl=self.sec_cache_name, input_filename=input_filename)

    def purge(self, key, version=None):

        if version is None:
            version = self.get(key)["version"]
            return self.purge(key, version)

        primer_obj = self.primer_obj(key)
        hints = HintsManager(cache_obj=self)


        primer_obj.do_hooks("pre_purge", key=key, hints=hints)
        hints.unset_hint_key(key=key)

        self._cache_delete(key, self.prim_cache_name, version=version)
        self._cache_delete(key, self.sec_cache_name, version=version)
        primer_obj.do_hooks("post_purge", key=key, hints=hints)
        return True

    def refresh(self, key, hints=None, queued=False, version=None, force_prime=False):
        """
        handles various aspects of the process of refreshing kck data

        :param key: the key associated with the data to be refreshed
        :param hints: an instance of HintsManager
        :param queued:
            if true, adds the refresh request to the queue and returns.
            if false, execute the refresh synchronously
        :param version:
            if provided, the version associated with the current key
            entry is checked against this param and, if it doesn't
            match, a VersionedRefreshMismatchException is raised
        :param force_prime:
            if true, causes a "from scratch" rebuild of the data.
            if false and there are hints in the HintsMgr, then
            attempt to "augment" the existing cache value
        :return:
        """

        logger.debug('ENTER refresh, key: {}'.format(key))
        # spin up a hints manager if one wasn't provided
        skip_augment = False
        if not hints:
            hints = HintsManager(self)
            skip_augment = True

        # queued request, update modified field in hints, queue request and return
        if bool(queued):
            return self.raw_queue_refresh(key=key, hints=hints, version=version)

        # get cache entry record or take note that it a
        key_set = True
        cache_entry_record = None
        try:
            cache_entry_record = hints.get(key)
        except KCKKeyNotSetException:
            key_set = False
            skip_augment = True

        if (version and not key_set) or (version and key_set and version != cache_entry_record['version']):
            raise VersionedRefreshMismatchException(key=key)

        # do pre-refresh hooks
        primer_obj = self.primer_obj(key)
        primer_obj.do_hooks("pre_refresh", key=key, hints=hints)

        # if there are hints, use them if possible to provide an augmented answer
        # (provides updated answer quicker)
        if not skip_augment:
            try:
                primer_obj.augment(key=key, hints=hints)
            except ComputeAugmentedValueNotImplemented:
                # cache_entry_record = self._prime(key)
                pass

        # if the hints.get() call above DID NOT result in a prime, then
        # prime and update hints
        cache_entry_record = self._prime(key)
        logger.debug('post-prime cache entry record: {}'.format(cache_entry_record))
        hints.set_hint_key(cache_entry_record)
        primer_obj.do_hooks("post_refresh", key=key, hints=hints)

        return cache_entry_record

    def primer_registered(self, name):
        return bool(name in self.primers)

    def register_primer(self, name, primer_obj):
        logger.info('registering primer: %s', name)
        primer_obj.set_cache(self)
        primer_obj.set_data(self.data_obj)
        primer_obj.set_name(name)
        self.primers[name] = primer_obj

    def _prime(self, key):

        try:
            primer_obj = self.primer_obj(key)

            primer_obj.do_hooks("pre_prime", key=key)

            primed_val = primer_obj.compute(key)
            logger.debug('primed_val: {}'.format(primed_val))

        except KCKKeyNotRegistered:
            raise KCKUnknownKey(key)

        ret = self._primcache_put_and_set_hooks(
            key, primed_val, primer_obj.expire, check_last_version=True, version=None)

        self._seccache_put(key, primed_val, primer_obj.expire)

        primer_obj.do_hooks("post_prime", key=key, hints=ret)

        return ret

    def _primcache_put_and_set_hooks(self, key, val, expire=None, version=None, check_last_version=None):
        primer_obj = None
        try:
            primer_obj = self.primer_obj(key)
            primer_obj.do_hooks("pre_set", key=key)
        except KCKKeyNotRegistered:
            logger.warning('_primcache_put_and_set_hooks - key: {} not registered'.format(key))
            # raise KCKUnknownKey(key)
        cache_entry = self._primcache_put(
            key, val, expire=expire, version=version, check_last_version=check_last_version)
        hints = HintsManager(cache_obj=self)
        hints.set_hint_key(cache_entry=cache_entry)
        if primer_obj:
            primer_obj.do_hooks("post_set", key=key, hints=hints)
        return cache_entry

    def _primcache_get(self, key):
        return self._cache_get(key, self.prim_cache_name)

    def _seccache_get(self, key, exc_class=None):
        return self._cache_get(key, self.sec_cache_name, exc_class)

    def _primcache_put(self, key, val, expire=None, version=None, check_last_version=None):
        logger.debug('setting primary cache for key: {}, value: {}'.format(key, val))
        return self._cache_put(key, self.prim_cache_name, val,
                               expire=expire, version=version,
                               check_last_version=check_last_version)

    def _seccache_put(self, key, val,
                      expire=None, version=None, check_last_version=None):
        return self._cache_put(key, self.sec_cache_name, val,
                               expire=expire, version=version,
                               check_last_version=check_last_version)

    def _cache_get(self, key, tbl, exc_class=None):

        exc_class = exc_class or KCKKeyNotSetException

        raw_get_result = self.raw_cache_get(key, tbl)

        try:
            return self.build_cache_entry_dict(
                key=key,
                version=raw_get_result[0][1],
                value=self.decomprickle(raw_get_result[0][0]),
                tbl=tbl,
                modified=raw_get_result[0][2],
                ttl=raw_get_result[0][3]
            )
        except IndexError:
            raise exc_class(key, tbl)

    def _cache_put(self, key, tbl, val,
                   version=None, check_last_version=None, expire=None):
        new_version = version if version is not None else self.gen_new_version()

        newval = self.comprickle(val)

        current_timestamp = datetime.datetime.utcnow()

        self.raw_cache_put(key, tbl, newval,
                           version=new_version, check_last_version=check_last_version,
                           expire=expire, modified=current_timestamp)
        ret = dict(success=True, version=new_version, key=key, value=val,
                   tbl=tbl, modified=current_timestamp)
        return ret

    def _cache_delete(self, key, tbl):
        self.raw_cache_delete(key, tbl)
        return dict(success=True, key=key, tbl=tbl)

    @classmethod
    def build_cache_entry_dict(cls, key, version, value, tbl, modified, ttl=None):
        ret = dict(
            success=True,
            version=version,
            key=key,
            value=value,
            tbl=tbl,
            modified=modified)
        if ttl:
            ret['ttl'] = ttl
        return ret
