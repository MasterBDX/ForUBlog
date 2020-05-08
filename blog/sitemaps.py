from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from posts.models import Post, Author, Category


class StaticViewsSitemaps(Sitemap):
    def items(self):
        return ['home', 'blog', 'about_me', 'about_blog', 'privacy_policy', 'contact_me']

    def location(self, item):
        return reverse(item)


class PostsViewsSitemap(Sitemap):
    def items(self):
        return Post.objects.all_active()

    def location(self, item):
        return item.get_absolute_url()


class AuthorViewsSitemap(Sitemap):
    def items(self):
        return Author.objects.all()

    def location(self, item):
        return item.get_absolute_url()


class CategoriesViewsSitemap(Sitemap):
    def items(self):
        return Category.objects.all()

    def location(self, item):
        return item.get_absolute_url()
