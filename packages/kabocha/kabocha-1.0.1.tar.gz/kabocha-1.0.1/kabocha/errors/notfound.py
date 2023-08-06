from .base import JsonError
from  .traceback import TracebackMixin

class NotFoundJsonError(JsonError):
    DEFAULTS = {
        'error_code' : 'not_found_error',
        'developer_message' : 'Not found',
        'user_message' : 'Not found',
        'status_code' : 404,
    }

class TracebackNotFoundJsonError(TracebackMixin, NotFoundJsonError):
    pass