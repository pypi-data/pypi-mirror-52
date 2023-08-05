import os

from kck.lib.kck_primer import KCKPrimer
from kck.lib.yaml_primer import KCKYamlPrimer
from kck.test.test_case import BasePostgresqlSeedingTestCase, BaseTestCacheTestCase, BaseKCKTestCase

SCRIPT_DIRPATH = os.path.dirname(os.path.realpath(__file__))
KCK_SOURCES_DIRPATH = os.path.join(SCRIPT_DIRPATH, "..")


class TestYamlPrimer(BaseKCKTestCase, BasePostgresqlSeedingTestCase, BaseTestCacheTestCase):
    def setup_method(self, method):
        self.setup_postgresql()
        self.setup_test_cache()

    def test_register_primer_yamls(self):
        """using a mock cache object, test that KCKYamlPrimer.register_primers()
            actually registers KCKYamlPrimers as it should"""

        # test that initially no primers are defined
        assert (self.cache_obj.no_primers_defined())

        # call register primers
        KCKYamlPrimer.register_primers(self.cache_obj)

        # assert that primers are now defined
        assert (not self.cache_obj.no_primers_defined())

        # assert that the simple1 primer is registered and that the first
        # parameter is named 'id'
        p = self.cache_obj.primer('simple1')
        assert (p is not None)
        assert (p.parameters[0]['name'] == 'id')

    def test_yml_primer_compute(self):
        """test that the compute method works for KCKYamlPrimers"""

        # get the simple1 primer
        KCKYamlPrimer.register_primers(self.cache_obj)
        p = self.cache_obj.primer('simple1')

        # test that the primer compute() returns expected result
        assert (
            p.compute('simple1' + KCKYamlPrimer.keysep + '1')[0][0] == 'homer')

    def test_yml_primer_result_jsonpath(self):
        """test jsonpath result processing for yml primers"""

        # get the simple_result_jsonpath primer
        KCKYamlPrimer.register_primers(self.cache_obj)
        p = self.cache_obj.primer("simple_result_jsonpath")

        # test that the primer compute() returns expected result
        assert (p.compute(
            "simple_result_jsonpath" + KCKYamlPrimer.keysep + "1") == "homer")

    def test_dict_rows(self):
        # get the simpledictrows primer
        KCKYamlPrimer.register_primers(self.cache_obj)
        p = self.cache_obj.primer("simpledictrows")

        # test that the primer compute() returns expected result
        compute_ret = p.compute("simpledictrows" + KCKYamlPrimer.keysep + "1")
        assert (compute_ret[0]["testcol1"] == "homer")


class TestKCKPrimer(BaseKCKTestCase, BasePostgresqlSeedingTestCase, BaseTestCacheTestCase):
    def setup_method(self, method):
        self.setup_postgresql()
        self.setup_test_cache()

    def test_register_primer_modules(self):
        """using the simple test cache object, test that KCKPrimer.register_primers()
            actually registers KCKPrimers as it should"""

        # assert no primers are defined
        assert (self.cache_obj.no_primers_defined())

        # call register_primers
        KCKPrimer.register_primers(self.cache_obj)

        # assert there are now primers defined
        assert (not self.cache_obj.no_primers_defined())

        # assert that the simpleclassbasedprimer1 primer is registered and that the first
        # parameter is named 'id'
        p = self.cache_obj.primer("simpleclassbasedprimer1")
        assert (p is not None)
        assert (p.parameters[0]["name"] == "id")

    def test_module_primer_compute(self):
        """test that the compute method works for KCKPrimers"""

        # get the simple1 primer
        KCKPrimer.register_primers(self.cache_obj)
        p = self.cache_obj.primer("simpleclassbasedprimer1")

        # test that the primer compute() returns expected result
        assert (
            p.compute("simpleclassbasedprimer1" + KCKYamlPrimer.keysep + "1")[
                0][0] == "marge")
