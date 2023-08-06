from .base import JsonError
from  .traceback import TracebackMixin

class ApplicationJsonError(JsonError):
    DEFAULTS = {
        'error_code' : 'application_error',
        'developer_message' : 'An unhandled application error ocurred.',
        'status_code' : 500,
    }

class TracebackApplicationJsonError(TracebackMixin, ApplicationJsonError):
    DEFAULTS = {
        'error_code' : 'traceback_application_error',
        'developer_message' : 'An unhandled application error ocurred.',
        'status_code' : 500,
    }