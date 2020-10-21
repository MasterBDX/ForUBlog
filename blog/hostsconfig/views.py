from django.http import HttpResponseRedirect
from django.conf import settings


def www_redirect_root(request,path=None):
    return HttpResponseRedirect(getattr(settings,'BASE_URL'))