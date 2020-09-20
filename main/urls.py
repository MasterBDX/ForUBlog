from django.urls import path
from .views import (
                    home_page_view, AboutMeView,
                    PostsDashboard,CategoriesDashboard,
                    AboutBlogView, PrivacyPolicyView, ContactUsView,
                    authors_admin_view,confirm_author_view,
                    )

app_name = 'main'
urlpatterns = [

    path('posts-dashboard/', PostsDashboard.as_view(), name='posts-dashboard'),
    path('categories-dashboard/', CategoriesDashboard.as_view(), name='categories-dashboard'),
    path('', home_page_view, name='home'),
    path('about_me', AboutMeView.as_view(), name='about_me'),
    path('about_blog', AboutBlogView.as_view(), name='about_blog'),
    path('privacy-policy', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('contact-us', ContactUsView.as_view(), name='contact_us')

    ]


urlpatterns += [
    path('authors_admin/', authors_admin_view, name='authors_admin'),


    path('confirm-author/<slug:slug>/',
         confirm_author_view, name='confirm_author')
]
