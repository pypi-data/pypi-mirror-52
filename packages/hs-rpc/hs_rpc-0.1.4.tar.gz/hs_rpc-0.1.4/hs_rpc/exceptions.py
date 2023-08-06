
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
        self.code = code