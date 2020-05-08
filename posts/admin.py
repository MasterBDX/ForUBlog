from django.contrib import admin

from .models import (Author, Category, Post)


class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['title']

    class Meta:
        model = Category


admin.site.register(Author)
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Post)
