import datetime
import logging

import copy
import dateutil
import random
from urllib.parse import urlencode

import pickle
import pytest
import csv

import cassandra
import dateutil
import zlib
from cassandra.cluster import Cluster, NoHostAvailable
from cassandra.connection import ConnectionException
from cassandra.policies import TokenAwarePolicy, RoundRobinPolicy
from dateutil.parser import parser
from cassandra.encoder import Encoder
from cassandra.util import sortedset

from simple_settings import settings

from kck.lib.exceptions import KCKKeyNotRegistered, KCKKeyNotSetException
from kck.lib.hints import HintsManager
from kck.lib.kck_database import KCKDatabase
from kck.lib.kck_primer import KCKPrimer
from kck.lib.kck_updater import KCKUpdater
from kck.lib.yaml_primer import KCKYamlPrimer
from kck.lib.yaml_updater import KCKYamlUpdater
import json
#from .config import kck_config_lookup


logger = logging.getLogger(__name__)


class PerformQueuedRefreshesRequiresRefreshSelectorException(Exception):
    pass


class VersionMismatchException(Exception):
    pass


class CassandraActor(object):
    prim_cache_name = None
    sec_cache_name = None
    update_queue_name = None
    refresh_queue_name = None
    refresh_counter_name = None
    refresh_selector_string = None
    cluster = None
    session = None
    cache_obj = None
    data_obj = None
    updaters = None
    primers = None
    keysep = "/"
    key_ver_sep = ':'
    tpickle = False
    tcompress = False

    UNCLAIMED_REFRESH_SELECTOR = 'unclaimed'
    DEFAULT_QUEUED_REFRESH_CHUNK_SIZE = 20
    QUEUE_TOO_SMALL_TO_SORT_MULT = 100
    REFRESH_COUNTS_TOO_SMALL_TO_DIFFERENTIATE = 5
    AVG_TO_MAX_SIMILARITY_THRESHOLD = 3

    def init(self,
             inhibit_framework_registration=False,
             cache_obj=None,
             data_obj=None,
             serialize=True,
             compress=True):
        try:
            self.session = self.cluster.connect(settings.KCK['cassandra']['keyspace'])
        except (ConnectionException, NoHostAvailable):
            self.cluster.shutdown()
            self._cache_create_keyspace(settings.KCK['cassandra']['keyspace'])
            self.cluster = Cluster(
                settings.KCK['cassandra']['hosts'],
                load_balancing_policy=RoundRobinPolicy(),
            )
            self.session = self.cluster.connect(settings.KCK['cassandra']['keyspace'])
        self._cache_create_table(self.prim_cache_name)
        self._cache_create_table(self.sec_cache_name)
        self._queued_updates_create_table(self.update_queue_name)
        self._queued_refreshes_create_tables(self.refresh_queue_name)

        self.cache_obj = cache_obj
        self.data_obj = data_obj

        if not inhibit_framework_registration:
            self._register_updaters()
            self._register_primers()

        self._register_hooks()

        self.tpickle = serialize
        self.tcompress = compress

    def decomprickle(self, val):
        ret = val
        # print("decom ret[{}]: {}".format(type(ret), ret))
        if self.tcompress:
            ret = zlib.decompress(ret)
        if self.tpickle:
            ret = pickle.loads(ret)["d"]
        return ret

    def comprickle(self, v):
        nv = v
        if self.tpickle:
            nv = pickle.dumps({"d": nv})
        if self.tcompress:
            nv = zlib.compress(nv)
        return nv

    def primitive_init(self):
        tbl_dict = settings.KCK['cassandra']['tables']
        self.prim_cache_name = tbl_dict['primary_cache']
        self.sec_cache_name = tbl_dict['secondary_cache']
        self.update_queue_name = tbl_dict['queued_updates']
        self.refresh_queue_name = tbl_dict['queued_refreshes']
        self.refresh_counter_name = tbl_dict['queued_refreshes_counter']
        self.cluster = Cluster(
            settings.KCK['cassandra']['hosts'],
            load_balancing_policy=RoundRobinPolicy(),
        )

        self.updaters = {}
        self.primers = {}

    def primer_obj(self, key):
        try:
            return self.cache_obj.primers[key.split(self.keysep)[0]]
        except KeyError:
            raise KCKKeyNotRegistered(key)

    def updater_obj(self, key):
        return self.data_obj.updaters[key.split(self.keysep)[0]]

    def do_processes(self):
        """call all primer processes in the cache"""

        PROCESS_DEF_TYPE_MAP = dict(
            sql=self._sql_process,
            key=self._key_process)

        # iterate over all primers in the cache
        for key, actor_obj in self.cache_obj.primers.items():

            # bail if the primer doesn't define processes
            try:
                processes = actor_obj.processes
            except AttributeError:
                continue

            # iterate over processes, calling each
            for process_name, process_dict in processes.items():
                print("process for key: {}, name: {}".format(
                    key, process_name))
                if process_dict["type"] in PROCESS_DEF_TYPE_MAP:
                    PROCESS_DEF_TYPE_MAP[process_dict["type"]](
                        process_name=process_name,
                        process_dict=process_dict,
                        actor_obj=actor_obj)

    def queue_refresh_count(self, key, version=None):
        """return the refresh request count for the key"""
        if version is None:
            q_fetch_record = (('select version from {} where kck_key = ?')
                              .format(self.refresh_queue_name))
            q_fetch_record_result = self.session.execute(
                self.session.prepare(q_fetch_record), (key, ))
            try:
                version = q_fetch_record_result[0][0]
            except IndexError:
                return 0

        q_fetch_count = (
            'select refresh_request_counter from {} where kck_key_version = ?'
            .format(self.refresh_counter_name))
        pq_fetch_count = self.session.prepare(q_fetch_count)
        q_fetch_count_result = self.session.execute(
            pq_fetch_count, (self._key_ver(key, version), ))
        try:
            return q_fetch_count_result[0][0]
        except IndexError:
            return 0

    def queued_refresh_data(self, selector=None, limit=None):

        logger.info('queued_refresh_data(selector={}, limit={})'.format(selector, limit))

        # ensure selector is defined
        selector = selector or self.UNCLAIMED_REFRESH_SELECTOR

        # --- get refresh counter stats
        pq_minmax_rowcount = self.session.prepare("""
            SELECT MIN(refresh_request_counter),
                   MAX(refresh_request_counter),
                   AVG(refresh_request_counter),
                   COUNT(*)
            FROM {}
        """.format(self.refresh_counter_name))
        fut_minmax_rowcount = self.session.execute(pq_minmax_rowcount)
        min_refresh_requests, max_refresh_requests,\
            avg_refresh_requests, num_refresh_requests = \
                fut_minmax_rowcount[0]

        # --- get counts table contents
        counts_table_dict = {}
        pq_counts = self.session.prepare("""
            SELECT kck_key_version, refresh_request_counter FROM {}
        """.format(self.refresh_counter_name))
        fut_counts = self.session.execute_async(pq_counts)
        counts_data = fut_counts.result()
        for key_version, counter in counts_data:
            key, version_as_str = key_version.split(self.key_ver_sep)
            version = int(version_as_str)

            if key not in counts_table_dict:
                counts_table_dict[key] = {}

            if version not in counts_table_dict[key]:
                counts_table_dict[key][version] = counter

        # limit isn't defined, so just grab everything that matches the selector
        if not limit:

            q_refresh_data = """
                SELECT kck_key, kck_hints, version
                FROM {} WHERE selector = '{}' ALLOW FILTERING
            """.format(self.refresh_queue_name)
            pq_refresh_data = self.session.prepare(q_refresh_data)
            refresh_data = self.session.execute(pq_refresh_data, (selector, ))

            refresh_dict = {}
            for key, hints, version in refresh_data:

                # logger.debug('CassandraActor::queued_refresh_data - raw hints: {}'.format(hints))

                refresh_dict[key] = {'version': version, 'count': 1, hints: self._decode_json(hints)}
                try:
                    refresh_dict[key]['count'] = counts_table_dict[key][version]
                except KeyError:
                    pass

            return refresh_dict

        # --- determine which refresh strategy to use
        refresh_strategy = None

        # strategy 1: num_refresh_requests is a small multiple of the
        #             limit
        if num_refresh_requests <= self.QUEUE_TOO_SMALL_TO_SORT_MULT * limit:
            refresh_strategy = 'most_requested'

        # strategy 2: max - min within threshold (switch to first requested
        #             from refresh table)
        elif max_refresh_requests - min_refresh_requests < self.REFRESH_COUNTS_TOO_SMALL_TO_DIFFERENTIATE:
            refresh_strategy = 'first_requested'

        # strategy 3: avg close to max (select only gte avg)
        elif max_refresh_requests - avg_refresh_requests <= self.AVG_TO_MAX_SIMILARITY_THRESHOLD:
            # q_counts += " WHERE refresh_request_counter > {}".format(
            #     avg_refresh_requests)
            refresh_strategy = 'first_requested_gte_avg'

        # strategy 4: (switch to first requested from refresh table)
        else:
            refresh_strategy = 'first_requested'

        logger.info('CassandraActor::queued_refresh_data - refresh strategy: {}'.format(refresh_strategy))

        # if strategy is most-requested and limit is defined,
        # limit to query
        if refresh_strategy == 'most_requested':

            # get refresh queue data
            pq_refresh_queue_data = self.session.prepare(
                """
                SELECT kck_key, kck_hints, version FROM {}
                WHERE selector = ?
                ALLOW FILTERING
            """.format(self.refresh_queue_name))
            refresh_queue_data = self.session.execute(pq_refresh_queue_data, (selector, ))

            # assemble all the refresh data with counts
            unsorted_refresh_data = {}
            for key, hints, version in refresh_queue_data:
                # logger.debug('CassandraActor::queued_refresh_data - raw hints: {}'.format(hints))
                unsorted_refresh_data[key] = {
                    'hints': self._decode_json(hints),
                    'version': version,
                    'count': 1
                }
                try:
                    unsorted_refresh_data[key]['count'] = counts_table_dict[
                        key][version]
                except KeyError:
                    pass

            # create a list of keys ordered by count
            ordered_keys_list = sorted(
                [k for k in unsorted_refresh_data],
                key=lambda x: unsorted_refresh_data[x]['count'],
                reverse=True)

            # clip the list as per the limit
            clipped_ordered_keys_list = ordered_keys_list[0:limit]

            clipped_refresh_queue_data = {}
            for key in clipped_ordered_keys_list:
                clipped_refresh_queue_data[key] = unsorted_refresh_data[key]

            return clipped_refresh_queue_data

        # build refresh queue data dict
        pq_refresh_queue_data = self.session.prepare("""
            SELECT kck_key, kck_hints, version, first_requested, last_requested FROM {}
            WHERE selector = ?
            ALLOW FILTERING
        """.format(self.refresh_queue_name))
        refresh_queue_data = self.session.execute(pq_refresh_queue_data,
                                                  (selector, ))
        unsorted_refresh_data = {}
        num_keys = 0
        total_count = 0
        for key, hints, version, first_req, last_req in refresh_queue_data:
            # logger.debug('CassandraActor::queued_refresh_data - raw hints: {}'.format(hints))
            unsorted_refresh_data[key] = {
                'hints': self._decode_json(hints),
                'version': version,
                'first_requested': first_req,
                'last_requested': last_req,
                'count': 1
            }
            try:
                unsorted_refresh_data[key]['count'] = counts_table_dict[key][
                    version]
            except KeyError:
                pass

            num_keys += 1
            total_count += unsorted_refresh_data[key]['count']

        # calc avg refresh request count
        avg_count = float(total_count) / float(num_keys)

        # determine eligible keys
        eligible_keys = None
        if refresh_strategy == 'first_requested_gte_avg':
            eligible_keys = []
            for key, refresh_dict in unsorted_refresh_data.items():
                if refresh_dict['count'] >= avg_count:
                    eligible_keys.append(key)
        else:
            eligible_keys = unsorted_refresh_data.keys()

        if refresh_strategy in ['first_requested_gte_avg', 'first_requested']:

            # create a list of keys ordered by last_requested
            ordered_keys_list = sorted(
                [k for k in eligible_keys],
                key=lambda x: unsorted_refresh_data[x]['first_requested'])

            # clip the list as per the limit
            clipped_ordered_keys_list = ordered_keys_list[0:limit]

            clipped_refresh_queue_data = {}
            for key in clipped_ordered_keys_list:
                clipped_refresh_queue_data[key] = unsorted_refresh_data[key]

            return clipped_refresh_queue_data

        raise Exception('unreachable code reached')

    def claim_refresh_requests(self, refresh_data):
        """
        set the selector on the refresh queue to the refresh_select_string
        for this instance, thus 'claiming' the refresh
        """
        slots = []
        for key, refresh_request_entry in refresh_data.items():
            # q = ("UPDATE {} " + "SET selector = ? " + "WHERE kck_key = ? " +
            #      "IF version = ? and selector = ?").format(self.refresh_queue_name)
            q = """
                UPDATE {}
                SET selector = ?
                WHERE kck_key = ? IF version = ? and selector = ?
            """.format(self.refresh_queue_name)
            pq = self.session.prepare(q)
            version = refresh_request_entry['version']
            fq = self.session.execute_async(
                pq, (self.refresh_selector_string, key, version,
                     self.UNCLAIMED_REFRESH_SELECTOR))
            slots.append((
                key,
                fq,
            ))
        return slots

    def perform_queued_refreshes(self, refresh_batch_size=None):

        if not self.refresh_selector_string:
            raise PerformQueuedRefreshesRequiresRefreshSelectorException

        refresh_batch_size = refresh_batch_size or self.DEFAULT_QUEUED_REFRESH_CHUNK_SIZE

        # get a batch of queued refreshes
        refresh_data = self.queued_refresh_data(limit=refresh_batch_size)

        logger.debug('refresh data: {}'.format(refresh_data))

        # claim refreshes with expectation that it will be only partially successful
        async_claim_requests = self.claim_refresh_requests(refresh_data)
        claim_request_result_list = []
        for key_fut_tuple in async_claim_requests:
            key, fut = key_fut_tuple
            result = fut.result()
            if result[0][0]:
                claim_request_result_list.append(key)

        logger.debug('claim request result list: {}'.format(claim_request_result_list))

        # perform refreshes for all the successful claims
        for key in claim_request_result_list:
            hints = None
            if 'hints' in refresh_data[key]:
                hints = HintsManager(self.cache_obj)
                hints.from_dict(refresh_data[key]['hints'])
            logger.debug('refreshing key: {}'.format(key))
            logger.debug('refreshing with hints: {}'.format(hints.to_dict()))
            self.cache_obj.refresh(key, hints=hints)

    def raw_queue_update(self, key, data):
        q = "insert into {} (kck_key, kck_data) values (?, ?)".format(
            self.update_queue_name)
        pq = self.session.prepare(q)
        future = self.session.execute_async(pq, (key, data))
        return future.result()

    def raw_cache_dump(self, tbl, output_filename):

        with open(output_filename, 'w', encoding='utf-8', newline='') as fh:
            csvwriter = csv.writer(fh)
            prepared_query = self.session.prepare(
                "select kck_key, kck_value, version, modified from {}".format(
                    tbl))
            future = self.session.execute_async(prepared_query)
            for row in future.result():
                processed_row = []
                for ndx, elem in enumerate(row):
                    if ndx == 1:
                        processed_row.append(json.dumps(self.decomprickle(elem)))
                        continue
                    processed_row.append(elem)
                # encoded_row = []
                # for raw_elem in row:
                #     elem = raw_elem
                #     print("type(elem) = {}".format(type(elem)))
                #
                #     if type(elem) is datetime.datetime:
                #         elem = elem.isoformat()
                #     elif type(elem) is int:
                #         elem = str(elem)
                #     if type(elem) is str:
                #         elem = elem.encode('utf-8')
                #     encoded_row.append(elem)
                #
                # csvwriter.writerow(tuple(encoded_row))
                csvwriter.writerow(processed_row)

    def raw_cache_load(self, tbl, input_filename):
        with open(input_filename, 'rt', encoding='utf-8') as fh:
            csvreader = csv.reader(fh)
            for row in csvreader:

                key, val, version, _ = row

                self.raw_cache_put(key,
                                   self.sec_cache_name,
                                   self.comprickle(json.loads(val)),
                                   int(version))

                # q = ('insert into {} (kck_key, kck_value, version, modified)'+
                #      'values (?, ?, ?, ?)').format(self.sec_cache_name)
                #
                # processed_row = []
                # for ndx, elem in enumerate(row):
                #     if ndx == 1:
                #         elem = self.comprickle(json.loads(elem))
                #     elif ndx == 2:
                #         elem = int(elem)
                #     elif ndx == 3:
                #         elem = dateutil.parser.parse(elem)
                #     processed_row.append(elem)
                #
                # pq = self.session.execute(q, processed_row)



    def raw_cache_put(self,
                      key,
                      tbl,
                      val,
                      version=None,
                      check_last_version=None,
                      expire=None,
                      modified=None):
        """sets the value associated with <key> in the table <tbl>.
           if callback_func is defined, the query is executed asynchronously
           and the future resulting from the call to execute_async method"""

        new_version = version if version is not None else self.gen_new_version(
        )

        ttl_clause = "" if expire is None else "using ttl {} ".format(
            expire.seconds)
        current_timestamp = datetime.datetime.utcnow(
        ) if modified == None else modified

        # --- if <check_last_version> is None, then don't do the version check
        if check_last_version is None:

            upsert_query = "update {} {}set kck_value = ?, version = ?, modified = ? where kck_key = ?".format(
                tbl, ttl_clause)
            prepared_query = self.session.prepare(upsert_query)
            future = self.session.execute_async(
                prepared_query, (val, new_version, current_timestamp, key))
            return future.result()

        # --- update only if version = <check_last_version>
        upsert_query = "update {} {}set kck_value = ?, version = ?, modified = ? where kck_key = ? if version = ?".format(
            tbl, ttl_clause)
        prepared_query = self.session.prepare(upsert_query)

        future = self.session.execute_async(
            prepared_query,
            (val, new_version, current_timestamp, key, check_last_version))

        return future.result()

    def raw_cache_delete(self, key, tbl, version=None):

        delete_query_str = "delete from {} where kck_key = ?".format(tbl)
        if version is None:
            return self.session.execute(
                self.session.prepare(delete_query_str), (key, ))
        delete_query_str += " and version = ?"
        return self.session.execute(
            self.session.prepare(delete_query_str), (key, version))

    def raw_cache_get(self, key, tbl):
        """looks up the value associated with <key> in the table <tbl>.
           if callback_func is defined, the query is executed asynchronously
           and the future resulting from the call to execute_async method"""
        prepared_query = self.session.prepare(
            "select kck_value, version, modified, TTL(kck_value) from {} where kck_key = ?".
            format(tbl))
        future = self.session.execute_async(prepared_query, (key, ))

        ret = future.result()
        return ret

    def raw_queue_refresh(self, key, version, hints=None):

        # fetch the refresh record for the key
        create_new_queue_entry = False
        if version is None:
            q_fetch_record = (('select kck_hints, version from {} ' +
                               'where kck_key = ?').format(
                                   self.refresh_queue_name))
            try:
                q_fetch_record_result = self.session.execute(
                    self.session.prepare(q_fetch_record), (key, ))
                version = q_fetch_record_result[0][1]
                # existing_hints_list_as_json = q_fetch_record_result[0][0]
                # existing_hints_list = self._decode_json(existing_hints_list_as_json)
                existing_hints_dict_as_json = q_fetch_record_result[0][0]
            except (IndexError, cassandra.InvalidRequest):
                create_new_queue_entry = True
                version = random.randint(0, 99999)

        # increment refresh counter (this is an upsert)
        q_inc = (('update {} ' +
                  'set refresh_request_counter = refresh_request_counter + 1 ' +
                  'where kck_key_version = ?').format(
                      self.refresh_counter_name))
        pq_inc = self.session.prepare(q_inc)
        inc_counter_query_result = self.session.execute(
            pq_inc, (self._key_ver(key, version), ))

        # if no refresh queue record exists, create a new refresh record
        # hints_as_str = self._to_encoded_json([hints.to_dict()]) if hints else None

        if create_new_queue_entry:
            nowts = datetime.datetime.utcnow()
            return self.session.execute(
                self.session.prepare(("""
                        update {}
                        set
                          selector = ?, first_requested = ?, last_requested = ?,
                          version = ?, kck_hints = ?
                        where kck_key = ?
                    """).format(self.refresh_queue_name)),
                (self.UNCLAIMED_REFRESH_SELECTOR, nowts, nowts, version,
                 self._to_encoded_json(hints.to_dict()), key))

        # if there's no hints, incrementing the refresh counter is good enough
        if hints is None:
            return True

        # if there are hints, update the hints list and increment the
        # refresh counter

        # # convert modified field in hints records to string
        # for hint in hints:
        #     if "modified" in hint:
        #         # hint["modified"] = str(hint["modified"])
        #         hint["modified"] = hint["modified"].isoformat()

        # try to insert a new record, if it fails update the old one
        new_version = random.randint(0, 99999)

        hints.import_from_dict(self._decode_json(existing_hints_dict_as_json))

        # new_hints = list(copy.copy(existing_hints_list))
        # if hints:
        #     new_hints.append(hints.to_dict())

        # new_hints = [*existing_hints_list, hints.to_dict()]
        # new_hints = []
        # for hint in existing_hints_dict:
        #     if hint:
        #         new_hints.append(self._to_encoded_json(hint))
        # for hint in hints:
        #     if hint:
        #         new_hints.append(self._to_encoded_json(hint))

        q_update_hints = """
            update {}
            set kck_hints = ?, last_requested = ?, version = ?
            where kck_key = ? if version = ?
        """.format(self.refresh_queue_name)
        pq_update_hints = self.session.prepare(q_update_hints)
        # future_hints = self.session.execute_async(
        #     pq_update_hints,
        #     ([self._to_encoded_json(new_hints)], datetime.datetime.utcnow(),
        #      new_version, key, version))
        # result = future_hints.result()
        result = self.session.execute(
            pq_update_hints,
            (self._to_encoded_json(hints.to_dict()),
             datetime.datetime.utcnow(),
             new_version, key, version))

        # return
        ret = result[0][0]
        return ret

    def _key_ver(self, key, version):
        return '{}{}{}'.format(key, self.key_ver_sep, version)

    def _to_encoded_json(self, d):
        def serialize_datetime(obj):
            if isinstance(obj, (datetime.datetime, datetime.date)):
                return obj.isoformat()
            raise TypeError("Type %s not serializable" % type(obj))

        as_json = json.dumps(d, default=serialize_datetime)
        #ret = Encoder().cql_encode_str(as_json)
        return as_json

    def _decode_json(self, json_str):
        return json.loads(json_str)

    def _key_process(self, process_name, process_dict, actor_obj):

        if "hooks" in process_dict:

            hooks = process_dict["hooks"]

            if "pre" in hooks and hooks["pre"] is not None:
                for pre_hook in hooks["pre"]:
                    pre_hook(self)

            if "value" in hooks and hooks["value"] is not None:
                for value_hook in hooks["value"]:
                    if "key_attribute" in process_dict:
                        key_ptr = getattr(actor_obj,
                                          process_dict["key_attribute"])
                        if callable(key_ptr):
                            key = key_ptr()
                        else:
                            key = key_ptr

                    if key is not None:
                        try:
                            value_hook(actor_obj,
                                       self.cache_obj.get(key)["value"])
                        except KCKKeyNotSetException:
                            pass

    def _sql_process(self, process_name, process_dict, actor_obj):

        if "hooks" in process_dict:

            hooks = process_dict["hooks"]

            if "pre" in hooks and hooks["pre"] is not None:
                for pre_hook in hooks["pre"]:
                    pre_hook(self)

            if "row" in hooks and hooks["row"] is not None:
                rowset = KCKDatabase.query(process_dict["database"],
                                           process_dict["query"])
                for row in rowset:
                    for row_hook in hooks["row"]:
                        row_hook(self, row)

            if "post" in hooks and hooks["post"] is not None:
                for post_hook in hooks["post"]:
                    post_hook(self)

    def _register_primers(self):
        """registers yaml and class-based primers"""
        KCKPrimer.register_primers(self.cache_obj)
        KCKYamlPrimer.register_primers(self.cache_obj)

    def _register_updaters(self):
        """registers yaml and class-based updaters"""
        KCKYamlUpdater.register_updaters(self.data_obj)
        KCKUpdater.register_updaters(self.data_obj)

    def _register_hooks(self):

        # register primer dependencies
        for _, p in self.primers.items():
            p.register_hooks()

        # register updater dependencies
        for _, u in self.updaters.items():
            u.register_hooks()

    def _cache_create_table(self, tbl):
        ks = settings.KCK['cassandra']['keyspace']
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS {}.{} (
              kck_key text PRIMARY KEY,
              kck_value blob,
              version int,
              modified timestamp,
            )
        """.format(ks, tbl))

    def _queued_updates_create_table(self, tbl):
        ks = settings.KCK['cassandra']['keyspace']
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS {}.{} (
              kck_key text PRIMARY KEY,
              kck_data blob,
              version int
            )
        """.format(ks, tbl))

    # counter explanation: https: // stackoverflow.com / questions / 23145817 / update - a - cassandra - integer - column - using - cql
    def _queued_refreshes_create_tables(self, tbl):
        ks = settings.KCK['cassandra']['keyspace']

        self.session.execute("""
            CREATE TABLE IF NOT EXISTS {}.{} (
              kck_key text PRIMARY KEY,
              selector text,
              first_requested timestamp,
              last_requested timestamp,
              kck_hints text,
              version int
            )
        """.format(ks, tbl))

        self.session.execute("""
            CREATE TABLE IF NOT EXISTS {}.{} (
              kck_key_version text PRIMARY KEY,
              refresh_request_counter counter
            )
        """.format(ks, tbl + "_counter"))

    @staticmethod
    def _cache_create_keyspace(keyspace_name):
        cluster = Cluster(settings.KCK['cassandra']['hosts'])
        create_keyspace_session = cluster.connect()
        create_keyspace_session.execute("""
            CREATE KEYSPACE IF NOT EXISTS {}
            WITH REPLICATION = {{
               'class' : 'SimpleStrategy',
               'replication_factor' : 1
            }}
        """.format(keyspace_name))
        create_keyspace_session.shutdown()
        cluster.shutdown()
