from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post

class StaticViewsSitemaps(Sitemap):
	def items(self):
		return Post.objects.all()

	def location(self, item):
		return item.get_absolute_url()