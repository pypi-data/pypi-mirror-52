import base64

from django.contrib.auth import authenticate, get_user_model

from tastypie.authentication import ApiKeyAuthentication, BasicAuthentication, MultiAuthentication

from .errors import UnauthorizedJsonError

class KabochaApiKeyAuthentication(ApiKeyAuthentication):
    def _unauthorized(self):
        return UnauthorizedJsonError()

    def is_authenticated(self, request, **kwargs):
        return super(KabochaApiKeyAuthentication, self).is_authenticated(request, **kwargs)

class KabochaBasicAuthentication(BasicAuthentication):
    def _unauthorized(self):
        return UnauthorizedJsonError()

class KabochaBasicAuthenticationWithInactiveUsers(KabochaBasicAuthentication):
    def _unauthorized(self):
        response = super(KabochaBasicAuthenticationWithInactiveUsers, self)._unauthorized()
        response.developer_message = 'The user could not be authenticated due to incorrect credentials, either because the user does not exist or because the credentials are wrong.'
        return response

    def is_authenticated(self, request, **kwargs):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return self._unauthorized()

        try:
            (auth_type, data) = request.META['HTTP_AUTHORIZATION'].split()
            if auth_type.lower() != 'basic':
                return self._unauthorized()
            user_pass = base64.b64decode(data).decode('utf-8')
        except:
            return self._unauthorized()

        bits = user_pass.split(':', 1)

        if len(bits) != 2:
            return self._unauthorized()

        if self.backend:
            user = self.backend.authenticate(username=bits[0], password=bits[1])
        else:
            user = authenticate(username=bits[0], password=bits[1])

        if user is None:
            UserModel = get_user_model()
            try:
                username = UserModel.objects.get(email=bits[0]).username
                if self.backend:
                    user = self.backend.authenticate(username=username, password=bits[1])
                else:
                    user = authenticate(username=username, password=bits[1])
                if user is None:
                    return self._unauthorized()
            except UserModel.DoesNotExist:                
                return self._unauthorized()

        request.user = user
        return True

class KabochaMultiAuthentication(MultiAuthentication):
    def is_authenticated(self, request, **kwargs):
        unauthorized = False

        for backend in self.backends:
            check = backend.is_authenticated(request, **kwargs)

            if check:
                if isinstance(check, UnauthorizedJsonError):
                    unauthorized = unauthorized or check
                else:
                    request._authentication_backend = backend
                    return check

        return unauthorized

ApiKeyAuthentication = KabochaApiKeyAuthentication
BasicAuthentication = KabochaBasicAuthentication
BasicAuthenticationWithInactiveUsers = KabochaBasicAuthenticationWithInactiveUsers
MultiAuthentication = KabochaMultiAuthentication