from django.core.exceptions import PermissionDenied
from functools import wraps


def super_user_only(function):

    @wraps(function)
    def inner(r, *args, **kwargs):
        user = r.user
        if not user.is_admin:
            raise PermissionDenied
        return function(r, *args, **kwargs)
    return inner
