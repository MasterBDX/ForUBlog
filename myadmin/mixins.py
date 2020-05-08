from django.core.exceptions import PermissionDenied


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        admin = request.user.is_admin
        if admin:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
