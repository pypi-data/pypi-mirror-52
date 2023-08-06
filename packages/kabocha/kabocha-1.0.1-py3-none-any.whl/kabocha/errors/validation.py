from .base import JsonError

DEFAULT_VALIDATION_ERROR = None

class ValidationJsonError(JsonError):
    DEFAULTS = {
        'error_code' : 'validation_failed',
        'developer_message' : "Validation of the submitted data failed. See 'validation_errors' for more information.",
        'user_message' :  'Data validation has failed.',
    }

    def __init__(self, validation_errors=DEFAULT_VALIDATION_ERROR, **kwargs):
        super(ValidationJsonError, self).__init__(**kwargs)
        self.validation_errors = validation_errors
    
    def validation_errors():
        doc = "Dictionary of fields that failed validation. Keys are the field names, values are lists of error messages. Defaults to '%s'" % DEFAULT_VALIDATION_ERROR

        def fget(self):
            return self.data['validation_errors']

        def fset(self, value):
            self.data['validation_errors'] = value
            self.update_content()

        def fdel(self):
            self.data['validation_errors'] = DEFAULT_VALIDATION_ERRORS
            self.update_content()

        return locals()
    validation_errors = property(**validation_errors())