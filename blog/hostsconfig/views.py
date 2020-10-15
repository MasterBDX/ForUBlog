from django.http import HttpResponseRedirect


def www_redirect_root(request,path=None):
    return HttpResponseRedirect('http://www.for4you.com:8000/')