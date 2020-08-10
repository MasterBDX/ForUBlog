from django.urls import path

from .views import (post_detail,posts_list_view, category_post_view, authors_post_view,
                    AddPostView, AddCategoryView, EditCategoryView, EditPostView, DeletePostView,
                    )

app_name = 'posts'
urlpatterns = [
    path('', posts_list_view, name='list'),
    path('add-post/', AddCategoryView.as_view(), name='add_category'),
    path('edit-category/<slug:slug>/',
         EditCategoryView.as_view(), name='edit_category'),
    path('add-category/', AddPostView.as_view(), name='add_post'),
    path('edit-post/<slug:post_slug>/', EditPostView.as_view(), name='edit_post'),
    path('delete-post/<slug:post_slug>/',
         DeletePostView.as_view(), name='delete_post'),
    path('<slug:slug>/', post_detail, name='detail'),
    path('categories/<slug:cat_slug>/posts',
         category_post_view, name='category_posts'),
    path('author/<slug:auth_slug>/posts',
         authors_post_view, name='author_posts'),
]
