from django.core.exceptions import PermissionDenied
from django.http import Http404


class AuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        author = request.user.is_author
        if author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class AuthorCheckMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=None)
        author = obj.author
        reuqest_author = self.request.user.author
        if author == reuqest_author or self.request.user.is_admin:
            return obj
        raise Http404


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        admin = request.user.is_admin
        if admin:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

from django.core.exceptions import PermissionDenied



