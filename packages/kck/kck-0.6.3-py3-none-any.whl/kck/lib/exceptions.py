import traceback


class BaseKCKException(Exception):

    msg = None

    def failure_info_dict(self):
        ret = dict(
            error=dict(
                name=self.__class__.__name__,
                args=self.args,
                traceback=traceback.format(self.__traceback__)
            )
        )

        if self.msg is not None:
            ret["error"]["message"] = self.msg

        return ret


class KCKKeyNotSetException(BaseKCKException):
    key = None
    tbl = None

    def __init__(self, key, tbl, msg="primer found, but compute() returned no results"):
        self.key = key
        self.tbl = tbl
        self.msg = msg


class KCKKeyNotRegistered(BaseKCKException):
    key = None

    def __init__(self, key):
        self.key = key


class UnexpectedPrimerType(BaseKCKException):
    pass


class KCKUnknownKey(BaseKCKException):
    key = None

    def __init__(self, key):
        self.key = key


class PrimerComputerReturnedNoResults(BaseKCKException):
    pass


class AuthTokenInvalid(BaseKCKException):
    msg = "Invalid authorization token"
    token = None

    def __init__(self, token):
        self.token = token


class AuthTokenExpired(BaseKCKException):
    msg = "Expire authorization token"
    token = None

    def __init__(self, token):
        self.token = token


class AuthHeaderNotPresent(BaseKCKException):
    msg = "Authorization header not present"


class AuthLoginUnknownUser(BaseKCKException):
    msg = "Unknown user or bad password"
    email = None

    def __init__(self, email):
        self.email = email


class AugmentError(BaseKCKException):
    msg = "Error encountered while augmenting cache entry"
    key = None

    def __init__(self, key, ):
        self.key = key

class RequestedAugmentationMethodDoesNotExist(BaseKCKException):
    msg = "Requested augmentation method does not exist"
    key = None
    requested_method = None

    def __init__(self, key, requested_method):
        self.key = key
        self.requested_method = requested_method


class CanNotAugmentWithoutVersion(BaseKCKException):
    msg = "To augment, one must first define."
    key = None

    def __init__(self, key, ):
        self.key = key


class CantAugmentUnknownPrimer(BaseKCKException):
    msg = "Requested primer instance was never registered"


class AugmentNotNecessaryException(BaseKCKException):
    msg = "No new hints found"


class VersionedRefreshMismatchException(BaseKCKException):
    msg = "version provided as parameter to refresh() does not match current entry version"
    key = None

    def __init__(self, key, ):
        self.key = key


class ComputeAugmentedValueNotImplemented(BaseKCKException):
    msg = "The primer associated with key: {} does not implement compute_augmented_value()"
    key = None

    def __init__(self, key, ):
        self.key = key