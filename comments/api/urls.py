from django.urls import path

from .views import (CommentListAPIView,AddCommentAPIView)

app_name = 'comments_api'

urlpatterns = [
	path('list/',CommentListAPIView.as_view(),name='list'),
	path('add/',AddCommentAPIView.as_view() ,name='add'),

]