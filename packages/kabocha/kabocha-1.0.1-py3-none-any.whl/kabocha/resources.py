import logging

from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.cache import patch_cache_control, patch_vary_headers
from django.utils import six
from django.core.signals import got_request_exception

from tastypie import fields
from tastypie.resources import Resource, ModelResource, sanitize
from tastypie.exceptions import ImmediateHttpResponse, NotFound, BadRequest, ApiFieldError
from tastypie.exceptions import UnsupportedFormat

from .errors import JsonError, UnauthorizedJsonError, ApplicationJsonError, NotFoundJsonError
from .errors import TracebackApplicationJsonError, TracebackNotFoundJsonError, ValidationJsonError

class KabochaResourceMixin(object):
    def is_authenticated(self, request):
        auth_result = self._meta.authentication.is_authenticated(request)

        if isinstance(auth_result, HttpResponse):
            raise ImmediateHttpResponse(response=auth_result)

        if not auth_result is True:
            raise ImmediateHttpResponse(response=UnauthorizedJsonError())

    def error_response(self, request, errors, response_class=JsonError, **kwargs):
        if errors:
            kwargs['additional_errors'] = self._meta.serializer.to_simple(errors, {})
        return response_class(**kwargs)

    def wrap_view(self, view):
        """
        Wraps methods so they can be called in a more functional way as well
        as handling exceptions better.
        Note that if ``BadRequest`` or an exception with a ``response`` attr
        are seen, there is special handling to either present a message back
        to the user or return the response traveling with the exception.
        """
        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            try:
                callback = getattr(self, view)
                response = callback(request, *args, **kwargs)

                # Our response can vary based on a number of factors, use
                # the cache class to determine what we should ``Vary`` on so
                # caches won't return the wrong (cached) version.
                varies = getattr(self._meta.cache, "varies", [])

                if varies:
                    patch_vary_headers(response, varies)

                if self._meta.cache.cacheable(request, response):
                    if self._meta.cache.cache_control():
                        # If the request is cacheable and we have a
                        # ``Cache-Control`` available then patch the header.
                        patch_cache_control(response, **self._meta.cache.cache_control())

                if request.is_ajax() and not response.has_header("Cache-Control"):
                    # IE excessively caches XMLHttpRequests, so we're disabling
                    # the browser cache here.
                    # See http://www.enhanceie.com/ie/bugs.asp for details.
                    patch_cache_control(response, no_cache=True)

                return response
            except BadRequest as e:
                data = {"developer_message": sanitize(e.args[0]) if getattr(e, 'args') else ''}
                return self.error_response(request, None, response_class=JsonError, **data)
            except fields.ApiFieldError as e:
                data = {"developer_message": sanitize(e.args[0]) if getattr(e, 'args') else ''}
                return self.error_response(request, None, response_class=ValidationJsonError, **data)
            except ValidationError as e:
                data = {"developer_message": sanitize(e.messages)}
                return self.error_response(request, None, response_class=ValidationJsonError, **data)
            except Exception as e:
                if hasattr(e, 'response'):
                    return e.response

                # A real, non-expected exception.
                # Handle the case where the full traceback is more helpful
                # than the serialized error.
                if settings.DEBUG and getattr(settings, 'TASTYPIE_FULL_DEBUG', False):
                    raise

                # Re-raise the error to get a proper traceback when the error
                # happend during a test case
                if request.META.get('SERVER_NAME') == 'testserver':
                    raise

                # Rather than re-raising, we're going to things similar to
                # what Django does. The difference is returning a serialized
                # error message.
                return self._handle_500(request, e)

        return wrapper

    def _handle_500(self, request, exception):
        import traceback
        import sys
        the_trace = '\n'.join(traceback.format_exception(*(sys.exc_info())))
        if settings.DEBUG:
            response_class = TracebackApplicationJsonError
        else:
            response_class = ApplicationJsonError
        response_code = 500

        NOT_FOUND_EXCEPTIONS = (NotFound, ObjectDoesNotExist, Http404)

        if isinstance(exception, NOT_FOUND_EXCEPTIONS):
            if settings.DEBUG:
                response_class = TracebackNotFoundJsonError
            else:
                response_class = NotFoundJsonError
            response_code = 404

        if settings.DEBUG:
            data = {
                "developer_message": sanitize(six.text_type(exception)),
                "traceback": the_trace,
            }
            return self.error_response(request, None, response_class=response_class, **data)

        # When DEBUG is False, send an error message to the admins (unless it's
        # a 404, in which case we check the setting).
        send_broken_links = getattr(settings, 'SEND_BROKEN_LINK_EMAILS', False)

        if not response_code == 404 or send_broken_links:
            log = logging.getLogger('django.request.tastypie')
            log.error('Internal Server Error: %s' % request.path, exc_info=True,
                      extra={'status_code': response_code, 'request': request})

        # Send the signal so other apps are aware of the exception.
        got_request_exception.send(self.__class__, request=request)

        return self.error_response(request, None, response_class=response_class)

    def deserialize(self, request, data, format='application/json'):
        """
        Given a request, data and a format, deserializes the given data.
        It relies on the request properly sending a ``CONTENT_TYPE`` header,
        falling back to ``application/json`` if not provided.
        Mostly a hook, this uses the ``Serializer`` from ``Resource._meta``.
        """
        format = request.META.get('CONTENT_TYPE', format)
        try:
            deserialized = self._meta.serializer.deserialize(data, format=format)
        except UnsupportedFormat as e:
            format = format.split(';')[0]
            if format == 'application/x-www-form-urlencoded':
                deserialized = request.POST.copy()
            elif format == 'multipart/form-data':
                deserialized = request.POST.copy()
                deserialized.update(request.FILES)
            else:
                raise e
        return deserialized

    def validate_form(self, form):
        if form.is_valid():
            return form
        else:
            raise self.form_error_response(form)

    def form_error_response(self, form):
        raise self.validation_error_response(form.errors)

    def validation_error_response(self, errors, **kwargs):
        raise ImmediateHttpResponse(response=ValidationJsonError(validation_errors=errors, **kwargs))

    def not_found_error_response(self):
        raise ImmediateHttpResponse(response=NotFoundJsonError())

    def unauthorized_error_response(self):
        raise ImmediateHttpResponse(UnauthorizedJsonError())

    def get_schema(self, request, **kwargs):
        """
        Returns a serialized form of the schema of the resource.
        Calls ``build_schema`` to generate the data. This method only responds
        to HTTP GET.
        Should return a HttpResponse (200 OK).
        Overriding the default Tastypie method so you don't need to authenticate
        as a user to see the schema.
        """
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        self.log_throttled_access(request)
        bundle = self.build_bundle(request=request)
        return self.create_response(request, self.build_schema())

class KabochaResource(KabochaResourceMixin, Resource):
    pass

class KabochaModelResource(KabochaResourceMixin, ModelResource):
    pass

class SimpleResourceMixin(object):
    def resource_uri_kwargs(self, bundle_or_obj=None):
        kwargs = super(SimpleResourceMixin, self).resource_uri_kwargs(bundle_or_obj)
        kwargs['resource_name'] = self._meta.parent_resource._meta.resource_name

        return kwargs

Resource = KabochaResource
ModelResource = KabochaModelResource