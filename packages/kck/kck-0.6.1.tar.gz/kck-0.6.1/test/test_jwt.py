import os
import json
from tornado.httputil import HTTPHeaders
from tornado.testing import AsyncHTTPTestCase
from urllib.parse import urlencode

_original_environment = None
if 'KCK_ENVIRONMENT' in os.environ:
    _original_environment = os.environ['KCK_ENVIRONMENT']

from kck.lib.kck_auth import KCKAuth, use_auth
from kck.lib.http_service import KCKHTTPServer
from kck.lib.kck_database import KCKDatabase
from kck.test.test_case import (BaseBlankCassandraTestCase,
                                BasePostgresqlSeedingTestCase,
                                BaseCacheInitTestCase,
                                BaseHTTPServerTestCase, BaseKCKTestCase)

from simple_settings import settings
from simple_settings.utils import settings_stub

import copy
ORIGINAL_KCK_SETTINGS = settings.KCK
new_kck_settings = copy.copy(ORIGINAL_KCK_SETTINGS)
new_kck_settings.update(dict(
    auth={
        'auth_user': 'auth/:email/:passwd_hash',
        'auth_user_list': 'auth_list',
        'secret': 'and8fjrysdgFGFS6CSue087dD778hdrtytyimnotnormallyaprayingmanbutifyoureuptherepleasesavemesuperman111289',
        'password_hash_salt': 'ohsotheyhaveinternetoncomputersnow'},
    use_auth=True))
AUGMENTED_KCK_SETTINGS = new_kck_settings


class TestHTTPServiceWithJWT(BaseKCKTestCase, AsyncHTTPTestCase,
                             BaseBlankCassandraTestCase,
                             BasePostgresqlSeedingTestCase,
                             BaseCacheInitTestCase,
                             BaseHTTPServerTestCase):

    def get_app(self):
        return KCKHTTPServer.get_instance(reset=True)

    @classmethod
    @settings_stub(KCK=AUGMENTED_KCK_SETTINGS)
    def setup_class(cls):
        use_auth(reset=True)
    #

    @classmethod
    @settings_stub(KCK=AUGMENTED_KCK_SETTINGS)
    def teardown_class(cls):
        use_auth(reset=True)

    @settings_stub(KCK=AUGMENTED_KCK_SETTINGS)
    def setup_method(self, method):
        self.setup_postgresql()
        self._delete_pgtable_auth()
        self.setup_cassandra()
        self.setup_cache()
        self._create_pgtable_auth()

    def _create_pgtable_auth(self):
        KCKDatabase.query(
            "test",
            """
                create table auth (
                    id serial PRIMARY KEY,
                    email varchar(256),
                    passwd varchar(256)
                )
            """
        )

    def _delete_pgtable_auth(self):
        KCKDatabase.query("test", "drop table if exists auth")

    def _insert_auth_row(self, userid, username, password):
        hashed_password = KCKAuth.get_instance().gen_password_hash(password)
        KCKDatabase.query(
            "test",
            """
                insert into auth
                (id, email, passwd)
                VALUES
                ({}, '{}', '{}')
            """.format(userid, username, hashed_password)
        )

    @settings_stub(KCK=AUGMENTED_KCK_SETTINGS)
    def test_jwt_login(self):
        # try to log in with the user credentials that haven't yet been
        #  entered and verify that it fails
        unknown_user_response = self.fetch(
            "/login/homer",
            method="POST",
            body=urlencode({"password": "blah"}).encode('utf-8'),
            headers=HTTPHeaders({'content-type': 'application/x-www-form-urlencoded'})
        )
        self.assert_response_is_error(unknown_user_response, name='AuthLoginUnknownUser')

        # add the user record to the auth table
        self._insert_auth_row(1, "homer", "blah")
        self.cache_obj.refresh('auth/homer/{}'.format(KCKAuth.get_instance().gen_password_hash('blah')))

        # try to log in again using the login credentials and verify that it works now
        known_user_response = self.fetch(
            "/login/homer",
            method="POST",
            body=urlencode({"password": "blah"}).encode('utf-8'),
            headers=HTTPHeaders({'content-type': 'application/x-www-form-urlencoded'})
        )
        known_user_response_data = json.loads(str(known_user_response.body, 'utf-8'))
        assert(bool(known_user_response_data["auth_token"]))

    @settings_stub(KCK=AUGMENTED_KCK_SETTINGS)
    def test_jwt_fetch(self):

        self._insert_auth_row(1, "homer", "blah")
        self.cache_obj.refresh('auth/homer/{}'.format(KCKAuth.get_instance().gen_password_hash('blah')))
        self.cache_obj.refresh('simple1/1')

        # try to log in again using the login credentials and verify that it works now
        login_response = self.fetch(
            "/login/homer",
            method="POST",
            body=urlencode({"password": "blah"}).encode('utf-8'),
            headers=HTTPHeaders({'content-type': 'application/x-www-form-urlencoded'})
        )
        self.assert_response_success(login_response)
        login_response_data = json.loads(str(login_response.body, 'utf-8'))
        assert("auth_token" in login_response_data)
        auth_token = login_response_data["auth_token"]

        # unauthed_response
        unauthed_response = self.fetch("/fetch/simple1/1")
        self.assert_response_is_error(unauthed_response, name='AuthHeaderNotPresent')

        # authed response
        authed_response = self.fetch(
            "/fetch/simple1/1",
            method="GET",
            headers=HTTPHeaders({'Authorization': auth_token})
        )
        self.assert_response_success(
            authed_response,
            key='simple1/1',
            value=[['homer', ], ]
        )

        # bad auth header response
        badhdr_response = self.fetch(
            "/fetch/simple1/1",
            method="GET",
            headers=HTTPHeaders({'Authorization': 'this.is.bad'})
        )
        self.assert_response_is_error(badhdr_response, name='AuthTokenInvalid', args=['this.is.bad'])

