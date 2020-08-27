from django.urls import path

from .views import (CommentListAPIView,AddCommentAPIView,EditCommentAPIView,
					DeleteCommentAPIView)

app_name = 'comments_api'

urlpatterns = [
	path('list/',CommentListAPIView.as_view(),name='list'),
	path('add/',AddCommentAPIView.as_view() ,name='add'),
	path('<int:pk>/edit/',EditCommentAPIView.as_view() ,name='edit'),
	path('<int:pk>/delete/',DeleteCommentAPIView.as_view() ,name='delete'),

]