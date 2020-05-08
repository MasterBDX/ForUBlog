from django.urls import path

from marketing.views import WebHookMailChimp

app_name = 'marketing'

urlpatterns = [
	path('webhook/',WebHookMailChimp.as_view(),name='webhook')
]