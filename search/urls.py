from django.urls import path

from .views  import search_posts_view, SearchUserView

app_name = 'search'
urlpatterns = [
    path('posts/',search_posts_view, name='posts'),
    path('users/',SearchUserView.as_view(), name='users')
]
