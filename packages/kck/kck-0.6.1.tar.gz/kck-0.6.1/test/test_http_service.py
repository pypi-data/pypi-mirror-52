import time
from tornado.httputil import HTTPHeaders
from tornado.testing import AsyncHTTPTestCase
from urllib.parse import urlencode
from kck.lib.http_service import KCKHTTPServer
from kck.lib.kck_auth import use_auth
from kck.lib.kck_cache import KCKCache
from kck.lib.kck_database import KCKDatabase
from kck.test.test_case import (
    BaseBlankCassandraTestCase, BasePostgresqlSeedingTestCase,
    BaseEnvironmentCheckingTestCase, BaseHTTPServerTestCase, BaseKCKTestCase)


class TestHTTPServer(BaseKCKTestCase, AsyncHTTPTestCase,
                     BaseBlankCassandraTestCase,
                     BasePostgresqlSeedingTestCase,
                     BaseEnvironmentCheckingTestCase, BaseHTTPServerTestCase):
    def setup_method(self, method):
        use_auth(reset=True)
        self.setup_cassandra()
        self.setup_postgresql()
        KCKCache.get_instance(new_instance=True)

    def get_app(self):
        return KCKHTTPServer.get_instance(reset=True)

    def test_fetch_known_unprimed_error(self):
        self.assert_response_is_error(
            self.fetch("/fetch/simple1/1"),
            name='KCKKeyNotSetException',
            args=['simple1/1', 'test__kck_sec_cache'])

    def test_fetch_unknown_unprimed_error(self):
        self.assert_response_is_error(
            self.fetch("/fetch/entirelyunknownkey1/1"),
            name='KCKUnknownKey',
            args=['entirelyunknownkey1/1'])

    def test_fetch_known_primed_success(self):
        KCKCache.get_instance().refresh('simple1/1')
        response = self.fetch("/fetch/simple1/1")
        self.assert_response_success(
            response, key='simple1/1', value=[
                [
                    'homer',
                ],
            ])

    def test_create(self):

        # create a new record
        res = self.fetch(
            "/create/simple_updater1",
            method="POST",
            body=urlencode({
                "testcol1": 2.345
            }),
            headers=HTTPHeaders({
                'content-type':
                'application/x-www-form-urlencoded'
            }))

        print("fetch result: {}".format(res))
        print("fetch result.data: {}".format(res.body))

        # test that the new record made it to the database
        result = KCKDatabase.query('test',
                                   'select testcol1 from testtbl1').fetchall()
        testcol1_values = [x[0] for x in result]
        assert ('2.345' in testcol1_values)

    def test_update(self):

        # create a record
        self.fetch(
            '/create/simple_updater1',
            method='POST',
            body=urlencode({
                'testcol1': 2.345}),
            headers=HTTPHeaders({
                'content-type':
                'application/x-www-form-urlencoded'}))

        time.sleep(1.5)

        # test create by querying the database
        result1 = KCKDatabase.query(
            'test', 'select id, testcol1 from testtbl1').fetchall()
        testcol1_values = [x[1] for x in result1]
        assert ('2.345' in testcol1_values)

        # update the newly created record
        self.fetch(
            '/update/simple_updater1',
            method='PUT',
            body=urlencode({
                'testcol1': 3.456,
                'id': result1[0][0]}),
            headers=HTTPHeaders({
                'content-type':
                'application/x-www-form-urlencoded'}))

        # test update by querying the database
        result2 = KCKDatabase.query(
            'test', 'select testcol1 from testtbl1 where id = {}'.format(
                result1[0][0])).fetchall()
        assert (result2[0][0] == '3.456')
