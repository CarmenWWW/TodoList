class TodoInfoException(Exception):
    ...


class TodoInfoNotFoundError(TodoInfoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Todo Not Found"


class TodoInfoAlreadyExistError(TodoInfoException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Todo Already Exists"
