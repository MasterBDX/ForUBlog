from django.urls import re_path,path,include

from .views import www_redirect_root

urlpatterns = [
    re_path(r'^(?P<path>.*)',www_redirect_root)    
    ]

