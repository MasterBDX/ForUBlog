from django.urls import path

from .views import (add_comment_view,
				    edit_comment_view,
				    delete_comment_view,
				    add_reply_view,
				    edit_reply_view,
				    delete_reply_view)
app_name = 'commetns'

urlpatterns = [
	path('add/',add_comment_view, name='add'),
	path('edit/<int:comment_pk>/',edit_comment_view,name='edit'),
	path('delete/<int:comment_pk>/',delete_comment_view,name='delete'),
	path('<int:comment_pk>/reply/add/',add_reply_view, name='add_reply'),
	path('<int:comment_pk>/reply/<int:reply_pk>/edit/',edit_reply_view,name='edit_reply'),
	path('<int:comment_pk>/reply/<int:reply_pk>/delete/',delete_reply_view,name='delete_reply'),

]