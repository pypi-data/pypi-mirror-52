from .base import JsonError

class UnauthorizedJsonError(JsonError):
    DEFAULTS = {
        'error_code' : 'unauthenticated',
        'developer_message' : 'The user could not be authenticated due to incorrect credentials (either because the user does not exist or because the credentials are wrong) or the user has not been activated.',
        'user_message' :  'Authentication failed.',
        'status_code' : 401,
    }