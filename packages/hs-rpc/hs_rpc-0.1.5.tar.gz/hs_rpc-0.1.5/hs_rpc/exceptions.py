class MissingConfigError(Exception):
    pass


class RpcFuncRegisterError(Exception):
    pass


class RpcError(Exception):
    code = None
    description = None

    def __init__(self, description=None, code=None):
        super(Exception, self).__init__()
        self.description = description
        if self.code is None:
            self.code = code

class NotFoundError(RpcError):
    code = 404


class AuthFailedError(RpcError):
    code = 401