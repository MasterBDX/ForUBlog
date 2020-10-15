from django.urls import path,include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from posts.views import posts_list_view

urlpatterns = [
    path('', admin.site.urls),
    ]



if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
