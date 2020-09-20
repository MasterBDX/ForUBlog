from django.contrib import admin

from .models import AboutMe, AboutBlog, PrivacyPolicy,MianImage,BlogInfo

admin.site.register(BlogInfo)
admin.site.register(AboutMe)
admin.site.register(AboutBlog)
admin.site.register(PrivacyPolicy)
admin.site.register(MianImage)
