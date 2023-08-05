import os
import yaml
import logging
from .err import handle_error, log_error

SCRIPT_DIRPATH = os.path.dirname(os.path.realpath(__file__))
KCK_SOURCES_DIRPATH = os.path.join(SCRIPT_DIRPATH, "..")

logger = logging.getLogger(__name__)


class NotEnoughParameters(Exception):
    pass


class FrameworkActor(object):

    keysep = "/"
    parameters = []
    cache_obj = None
    data_obj = None
    hooks = None
    name = None

    @staticmethod
    def make_relpath_absolute(dirpath):
        """given any dirpath, relative or absolute, return an absolute dirpath"""
        if dirpath[0] == '/':
            return dirpath
        return os.path.abspath(os.path.join(KCK_SOURCES_DIRPATH, dirpath))

    @staticmethod
    def proc_files_in_dirpath(dirpath, filter_func, callback_func):
        """walk all files in dirpath, recursing into subdirs, and, if filter_func
           returns True for a given filepath, call callback_func with the filepath
           as a parameter"""
        for subdir, dirs, files in os.walk(dirpath):
            for file in files:
                fp = os.path.join(subdir, file)
                if filter_func(fp):
                    callback_func(os.path.join(subdir, file))

    @staticmethod
    def read_yaml(filepath, on_error=None):
        """read/parse a yaml file, return resulting object"""
        with open(filepath, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                handle_error(exc, "unable to init config object", on_error)

    def set_name(self, name_str):
        self.name = name_str

    def get_name(self):
        return self.name

    def set_cache(self, cache_obj):
        self.cache_obj = cache_obj

    def get_cache(self):
        return self.cache_obj

    def set_data(self, data_obj):
        self.data_obj = data_obj

    def get_data(self):
        return self.data_obj

    def primary_key_parameter_name(self):
        for p in self.parameters:
            if "primary_key" in p and bool(p["primary_key"]):
                return p["name"]
        return None

    def dependency_key(self):
        ret = self.name
        for p in self.parameters:
            ret += self.keysep + ":{}".format(p["name"])
        return ret

    def dependency_key_to_param_dict(self, key_tmpl, key):
        key_tmpl_names_with_colons = \
            key_tmpl.split(self.keysep) if self.keysep in key_tmpl else [key_tmpl]
        key_tmpl_names = \
            [ x.split(':')[1] if ':' in x else x for x in key_tmpl_names_with_colons][1:]
        key_values = key.split(self.keysep)[1:] if self.keysep in key else [key]

        ret = {}
        for ndx, name in enumerate(key_tmpl_names):
            ret[name] = key_values[ndx]

        return ret

    def key_to_param_dict(self, key_str):

        def build_partial_param_dict():
            # this builds the dict when there's no primary key (as when records
            #  are being created)

            if len(param_value_list) == 0:
                return {}

            # if there's just one arg, it's the primary key and we're updating
            if len(param_value_list) == 1:
                primary_key_name = None
                for ndx, param_dict in enumerate(self.parameters):
                    if "primary_key" in param_dict and bool(param_dict["primary_key"]):
                        primary_key_name = param_dict["name"]
                        return {primary_key_name: param_value_list[0]}

            # build return dict
            ret = {}
            offset = 0
            for ndx, param_dict in enumerate(self.parameters):

                # skip the primary key since it's not defined for partials
                if "primary_key" in param_dict and bool(param_dict["primary_key"]):
                    offset = -1
                    continue

                # set return dict key/value
                ret[param_dict["name"]] = param_value_list[ndx + offset]

                if "type" in param_dict:
                    param_type = param_dict['type']
                    param_name = param_dict['name']
                    try:
                        ret[param_name] = transform[param_type](ret[param_name])
                    except ValueError:
                        ret[param_name] = None
                    except KeyError:
                        logger.warn(
                            'key_to_param_dict - ' +
                            'stated parameter type: {} for key: {}'.format(
                                param_type, key_str) +
                            ') has no registered transformation')
            return ret

        # if there's no key, then return an empty dict
        if key_str is None or key_str == "":
            return {}

        # break the key into a list
        param_value_list = key_str.split(self.keysep)[1:] if self.keysep in key_str else []

        # validate length of params
        if len(param_value_list) < len(self.parameters):
            build_partial_param_dict()

        # post-processing for params since they're strings as part of the key
        transform = dict(
            str=lambda x: str(x),
            string=lambda x: str(x),
            float=lambda x: float(x),
            int=lambda x: int(x))

        # iterate through key components, building parameter dict
        ret = {}
        for ndx, param_dict in enumerate(self.parameters):
            # determine name of the parameter
            varname = param_dict["name"]
            # set dict value to key component value
            try:
                ret[varname] = param_value_list[ndx]
            except IndexError:
                logger.error(
                    "key({}) doesn't contain enough data: params=({})".format(
                        key_str,
                        self.parameters
                    )
                )
                raise

            # if type is in the param_dict, transform the value
            if "type" in param_dict:
                transform_func = transform[param_dict['type']]
                ret[varname] = transform_func(ret[varname])

        return ret

    def param_dict_to_key(self, param_dict):
        key_components = []
        for p in self.parameters:
            try:
                key_components.append(str(param_dict[p["name"]]))
            except KeyError:
                raise NotEnoughParameters
        return self.keysep.join(key_components)

    def register_hooks(self):
        if self.hooks is None:
            self.hooks = {}

    def add_hook(self, event, keystr, func):
        if self.hooks is None:
            self.hooks = {}
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append((keystr, func))

    def do_hooks(self, event, *args, **kwargs):

        if self.hooks is None:
            self.hooks = {}

        try:
            for hook_tuple in self.hooks[event]:
                keystr, hfunc = hook_tuple
                logger.debug("  found {} hook named {} with key: {}...".format(event, hfunc.__name__, keystr))
                kwargs["param_key"] = keystr
                try:
                    hfunc(*args, **kwargs)
                except Exception as e:
                    logger.error(e)

        except KeyError:
            pass
