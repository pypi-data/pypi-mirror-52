import json

from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

DEFAULT_ERROR_CODE = "no_code"
DEFAULT_DEVELOPER_MESSAGE = "No error message available."
DEFAULT_USER_MESSAGE = "An error has occurred."
DEFAULT_MORE_INFO = None
DEFAULT_STATUS_CODE = 400
DEFAULT_ADDITIONAL_ERRORS = None

class BaseJsonError(JsonResponse):
    def __init__(self, error_code=DEFAULT_ERROR_CODE, developer_message=DEFAULT_DEVELOPER_MESSAGE, user_message=DEFAULT_USER_MESSAGE, more_info=DEFAULT_MORE_INFO, status_code=DEFAULT_STATUS_CODE, additional_errors=DEFAULT_ADDITIONAL_ERRORS, encoder=DjangoJSONEncoder, **kwargs):
        data = {
            "error_code" : error_code,
            "developer_message" : developer_message,
            "user_message" : user_message,
            "more_info" : more_info,
            "status_code" : status_code,
            "additional_errors" : additional_errors,
        }
        self.encoder = encoder
        self.data = data
        super(BaseJsonError, self).__init__(data, status=status_code, encoder=encoder, **kwargs)

    def update_content(self):
        self.content = json.dumps(self.data, cls=self.encoder)

    def error_code():
        doc = "Short error code that uniquely identifies the error. Defaults to '%s'" % DEFAULT_ERROR_CODE

        def fget(self):
            return self.data['error_code']

        def fset(self, value):
            self.data['error_code'] = value
            self.update_content()

        def fdel(self):
            self.data['error_code'] = DEFAULT_ERROR_CODE
            self.update_content()

        return locals()
    error_code = property(**error_code())

    def developer_message():
        doc = "Verbose description of the error for the developer's benefit. Defaults to '%s'" % DEFAULT_DEVELOPER_MESSAGE

        def fget(self):
            return self.data['developer_message']

        def fset(self, value):
            self.data['developer_message'] = value
            self.update_content()

        def fdel(self):
            self.data['developer_message'] = DEFAULT_DEVELOPER_MESSAGE
            self.update_content()

        return locals()
    developer_message = property(**developer_message())

    def user_message():
        doc = "Verbose error message that can be passed on to the user if not otherwise handled. Defaults to '%s'" % DEFAULT_USER_MESSAGE

        def fget(self):
            return self.data['user_message']

        def fset(self, value):
            self.data['user_message'] = value
            self.update_content()

        def fdel(self):
            self.data['user_message'] = DEFAULT_USER_MESSAGE
            self.update_content()

        return locals()
    user_message = property(**user_message())

    def more_info():
        doc = "URL to a document that provides more information about the error. Defaults to '%s'" % DEFAULT_MORE_INFO

        def fget(self):
            return self.data['more_info']

        def fset(self, value):
            self.data['more_info'] = value
            self.update_content()

        def fdel(self):
            self.data['more_info'] = DEFAULT_MORE_INFO
            self.update_content()

        return locals()
    more_info = property(**more_info())

    def status_code():
        doc = "HTTP status code of the response. Defaults to '%s'" % DEFAULT_STATUS_CODE

        def fget(self):
            return self.data['status_code']

        def fset(self, value):
            self.data['status_code'] = value
            self.status = value
            self.update_content()

        def fdel(self):
            self.data['status_code'] = DEFAULT_STATUS_CODE
            del self.status
            self.update_content()

        return locals()
    status_code = property(**status_code())

    def additional_errors():
        doc = "Additional error information, to hold other information provided by the system that may not be handled otherwise. Defaults to '%s'" % DEFAULT_ADDITIONAL_ERRORS

        def fget(self):
            return self.data['additional_errors']

        def fset(self, value):
            self.data['additional_errors'] = value
            self.update_content()

        def fdel(self):
            self.data['additional_errors'] = DEFAULT_ADDITIONAL_ERRORS
            self.update_content()

        return locals()
    additional_errors = property(**additional_errors())

class JsonError(BaseJsonError):
    DEFAULTS = {}

    def __init__(self, **kwargs):
        new_kwargs = self.DEFAULTS.copy()
        new_kwargs.update(kwargs)
        super(JsonError, self).__init__(**new_kwargs)