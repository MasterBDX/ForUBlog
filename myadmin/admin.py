from django.contrib import admin

from myadmin.models import AboutMe, AboutBlog, PrivacyPolicy

admin.site.register(AboutMe)
admin.site.register(AboutBlog)
admin.site.register(PrivacyPolicy)
