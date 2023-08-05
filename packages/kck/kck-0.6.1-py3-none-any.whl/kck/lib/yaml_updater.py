import os

from .kck_updater import KCKUpdater
from simple_settings import settings
from .yaml_reader import YAMLReader


class KCKYamlUpdater(KCKUpdater, YAMLReader):

    def __init__(self, yaml_filepath):
        self.filepath = yaml_filepath
        self._proc_updater_yaml()

    @classmethod
    def register_updaters(cls, data_obj):
        """register all yaml-based updaters in the updaters dir"""
        def fnfilter(filepath):
            if filepath[-4:] == ".yml":
                return True
            return False

        def proc_primer_yaml(filepath):
            data_obj.register_updater(
                os.path.basename(filepath)[:-4],
                KCKYamlUpdater(filepath))

        cls.proc_files_in_dirpath(
            cls.make_relpath_absolute(settings.KCK['updaters_dirpath']),
            fnfilter,
            proc_primer_yaml)

    def register_hooks(self):
        # register after_primes refreshes
        super(KCKYamlUpdater, self).register_hooks()

    def _proc_updater_yaml(self):

        u = self.read_yaml(self.filepath)

        self.name = [os.path.basename(self.filepath)[:-4]]
        self.database = u["database"]
        self.parameters = u["parameters"]
        self.query_template = u["query"]["template"]
