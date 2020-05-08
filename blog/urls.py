from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap

from .views import (home_page_view, blog_view, AboutMeView,
                    AboutBlogView, PrivacyPolicyView, ContactMeView)

from .sitemaps import (StaticViewsSitemaps,
                       PostsViewsSitemap,
                       AuthorViewsSitemap,
                       CategoriesViewsSitemap)

sitemaps = {'static': StaticViewsSitemaps,
            'posts': PostsViewsSitemap,
            'author_posts': AuthorViewsSitemap,
            'cats': CategoriesViewsSitemap}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path(r'tinymce/', include('tinymce.urls')),
    path('mailchimp/', include('marketing.urls', namespace='mailchimp')),
    path('<slug:post_slug>/comments/',
         include('comments.urls', namespace='comments')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('account/', include('accounts.urls', namespace='account')),
    path('accounts/', include('accounts.passwords.urls')),
    path('myadmin/', include('myadmin.urls', namespace='myadmin')),
    path('search/', include('search.urls', namespace='search')),
    path('', home_page_view, name='home'),
    path('posts/', blog_view, name='blog'),
    path('about_me', AboutMeView.as_view(), name='about_me'),
    path('about_blog', AboutBlogView.as_view(), name='about_blog'),
    path('privacy-policy', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('contact-us', ContactMeView.as_view(), name='contact_me')]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
