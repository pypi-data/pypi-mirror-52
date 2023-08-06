import datetime

from kck.lib.hints import HintsManager
from kck.lib.kck_cache import KCKCache
from kck.lib.kck_primer import KCKPrimer
import types


def NoDataAvailable(Exception):
    key = None

    def __init__(self, key):
        self.key = key


def get_decorator_primer(keys, compute_func):
    def compute_with_self_and_args(self, keystr):
        args = keystr.split(KCKCache.keysep)[1:]
        if args:
            return compute_func(*args)
        return compute_func()

    p = KCKPrimer()
    p.keys = keys
    p.compute = types.MethodType(compute_with_self_and_args, p)
    return p


class kckprime:

    dargs = None
    dkwargs = None

    def __init__(self, *args, **kwargs):
        self.dargs = args
        self.dkwargs = kwargs

    def __call__(self, f, *args, **kwargs):
        def cache_lookup(*args, **kwargs):
            cache_obj = KCKCache.get_instance()

            if args:
                key = "{}{}{}".format(self.dkwargs["name"], cache_obj.keysep,
                                      cache_obj.keysep.join(args))
            else:
                key = self.dkwargs["name"]
            response = cache_obj.get(key, prime_on_cache_miss=True)
            if bool(response["success"]):
                return response["value"]
            raise NoDataAvailable(key)

        def df(*args, **kwargs):
            # set up primer
            keys = self.dkwargs["keys"] if "keys" in self.dkwargs else None
            name = self.dkwargs["name"]

            cache_obj = KCKCache.get_instance()
            if not cache_obj.primer_registered(name):
                cache_obj.register_primer(name, get_decorator_primer(keys, f))

            return cache_lookup(*args, **kwargs)

        return df


class kckrefresh:
    dargs = None
    dkwargs = None

    def __init__(self, *args, **kwargs):

        # store the decorator args
        self.dargs = args
        self.dkwargs = kwargs

    def __call__(self, f, *args, **kwargs):

        # function wrapper
        def df(*args, **kwargs):

            # call the function and get the result
            ret = f(*args, **kwargs)

            # build the parameter dict using the param_keys and the args to the decorated function
            param_dict = {}
            if 'param_keys' in self.dkwargs:
                for compute_param_name, param_name in self.dkwargs["param_keys"].items():
                    param_dict[compute_param_name] = kwargs[param_name]

            # build the list of params which will become the key
            key_param_list = []
            if "keys" in self.dkwargs:
                for param_name in self.dkwargs["keys"]:
                    key_param_list.append(param_dict[param_name])

            cache_obj = KCKCache.get_instance()

            name = self.dkwargs["name"]
            keys = self.dkwargs["keys"] if "keys" in self.dkwargs else []
            if not cache_obj.primer_registered(name) and "compute" in self.dkwargs:
                cache_obj.register_primer(
                    name,
                    get_decorator_primer(keys, self.dkwargs["compute"]))

            # compute refresh key
            refresh_key = name
            if key_param_list:
                refresh_key = "{}{}{}".format(
                    name, cache_obj.keysep, cache_obj.keysep.join(key_param_list))

            # build refresh params that are default False
            hints = HintsManager(cache_obj)
            for param_name in ['queued', 'force_prime']:
                param_value = False
                if param_name in self.dkwargs and self.dkwargs[param_name]:
                    param_value = self.dkwargs[param_name]
                hints.set_hint_key(
                    cache_obj.build_cache_entry_dict(
                        key=param_name,
                        version=None,
                        value=param_value,
                        tbl=cache_obj.prim_cache_name,
                        modified=datetime.datetime.utcnow()))

            cache_obj.refresh(refresh_key, hints, queued=self.dkwargs.get('queued', False))

            return ret

        return df
