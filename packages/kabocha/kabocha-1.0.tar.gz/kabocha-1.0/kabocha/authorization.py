from django.db.models import Q

from tastypie.authorization import Authorization

def get_module_name(meta):
    return getattr(meta, 'model_name', None) or getattr(meta, 'module_name')

class GuardianAuthorization(Authorization):
    def base_checks(self, request, model_klass):
        # If it doesn't look like a model, we can't check permissions.
        if not model_klass or not getattr(model_klass, '_meta', None):
            return False
        # User must be logged in to check permissions.
        if not hasattr(request, 'user'):
            return False
        return model_klass

    def get_filter(self, klass, user, permission_codename):
        UserPermissionModel = getattr(klass, 'user_object_permission_model', None)
        if UserPermissionModel:
            object_ids = list(UserPermissionModel.objects.filter(user=user).values_list('content_object_id', flat=True))
        else:
            object_ids = []
        return Q(Q(user=user) | Q(id__in=object_ids))

    def generic_list(self, object_list, request, permission_code):
        klass = self.base_checks(request, object_list.model)
        if klass is False:
            return object_list.none()
        permission = '%s_%s' % (permission_code, get_module_name(klass._meta))
        return object_list.filter(self.get_filter(klass, request.user, permission)).distinct()

    def generic_detail(self, obj, request, permission_code):
        klass = self.base_checks(request, obj.__class__)
        if klass is False:
            return False
        if obj.user == request.user:
            return True
        permission = '%s_%s' % (permission_code, get_module_name(klass._meta))
        if not request.user.has_perm(permission, obj):
            return False
        return True

    def read_list(self, object_list, bundle):
        return self.generic_list(object_list, bundle.request, 'view')

    def read_detail(self, object_list, bundle):
        return self.generic_detail(bundle.obj, bundle.request, 'view')

    def update_list(self, object_list, bundle):
        return self.generic_list(object_list, bundle.request, 'change')

    def update_detail(self, object_list, bundle):
        return self.generic_detail(bundle.obj, bundle.request, 'change')

    def delete_list(self, object_list, bundle):
        return self.generic_list(object_list, bundle.request, 'delete')

    def delete_detail(self, object_list, bundle):
        return self.generic_detail(bundle.obj, bundle.request, 'delete')