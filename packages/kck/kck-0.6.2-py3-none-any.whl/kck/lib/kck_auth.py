import hashlib

import datetime

import jwt
from simple_settings import settings
# from kck.lib.config import kck_config_lookup
from kck.lib.exceptions import AuthTokenInvalid, AuthTokenExpired

authed_userid = None
_auth_instance_obj = None
# try:
#     use_auth = kck_config_lookup("kck", "enable_auth")
# except KeyError:
#     use_auth = False

_use_auth = None
def use_auth(reset=False):
    global _use_auth
    if _use_auth is None or reset:
        try:
            _use_auth = bool(settings.KCK['use_auth'])
        except KeyError:
            _use_auth = False
    return _use_auth


class AuthDisabled(Exception):
    pass


class KCKAuth(object):

    auth_secret = None
    password_hash_salt = None
    use_auth = False

    @classmethod
    def get_instance(cls):
        global _auth_instance_obj
        if _auth_instance_obj is None:
            _auth_instance_obj = KCKAuth(settings.KCK['auth'])
        return _auth_instance_obj

    def __init__(self, auth_dict):

        self.auth_dict = auth_dict
        if use_auth():
            self.auth_secret = self.auth_dict['secret']
            self.password_hash_salt = self.auth_dict['password_hash_salt']
            self.use_auth = True

    def gen_password_hash(self, passwd):
        if not self.use_auth:
            raise AuthDisabled
        salt = self.password_hash_salt.encode("utf-8")
        salted_passwd = salt+passwd.encode("utf-8") if type(passwd) is str else salt+passwd
        return hashlib.md5(salted_passwd).hexdigest()

    def type(self):
        return self.auth_dict["type"]

    def userid_to_authtoken(self, user_id):
        currtime = datetime.datetime.utcnow()
        return jwt.encode(
            {
                'exp': currtime + datetime.timedelta(days=0, seconds=5),
                'iat': currtime,
                'sub': user_id
            },
            self.auth_secret,
            algorithm='HS256'
        )

    def authtoken_to_userid(self, token):
        try:
            return jwt.decode(
                token,
                self.auth_secret
            )['sub']
        except jwt.ExpiredSignatureError:
            raise AuthTokenExpired(token)
        except jwt.InvalidTokenError:
            raise AuthTokenInvalid(token)

    def authed_userid(self, userid=None):
        global authed_userid
        if userid is not None:
            authed_userid = userid
        return authed_userid