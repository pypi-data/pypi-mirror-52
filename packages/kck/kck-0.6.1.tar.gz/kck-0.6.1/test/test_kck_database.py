from kck.lib.kck_database import KCKDatabase
from kck.test.test_case import BaseEnvironmentCheckingTestCase, BaseKCKTestCase


class TestKCKDatabase(BaseKCKTestCase, BaseEnvironmentCheckingTestCase):

    def test_simple_query(self):
        response = KCKDatabase.query("test", "select 1")
        print("response: {}".format(response))


