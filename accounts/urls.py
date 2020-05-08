from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from .views import (UserLoginView, UserLogoutView,EmailActivationView,
                    UserRegistrerView,profile_view,DeleteUserView)

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login' ),
    path('logout/', UserLogoutView.as_view(), name='logout' ),
    path('register/', UserRegistrerView.as_view(), name='register' ),
    path('profile/<slug:user_slug>/', profile_view, name='profile' ),
    path('delete/<slug:user_slug>/', DeleteUserView.as_view(), name='delete' ),
    re_path(r'^email-confirm/(?P<key>[0-9a-zA-Z]+)/$', EmailActivationView.as_view(), name='email-activate' ),
    path('email-resend-activation/', EmailActivationView.as_view(), name='email-resend-activation' ),
    

 # password settings

]
