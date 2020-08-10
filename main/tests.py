from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse , resolve

from . import  views


class TestBlogUrls(SimpleTestCase):

    def test_home_and_blog_url(self):
        home_url = reverse('home')
        blog_url = reverse('blog')
        self.assertEquals(resolve(home_url).func, views.home_page_view)
        self.assertEquals(resolve(blog_url).func, views.blog_view)


class TestBlogViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_response = self.client.get(reverse('home'))
        self.blog_response = self.client.get(reverse('blog'))


    def test_home_view(self):
        #  response tests
        self.assertEquals(self.blog_response.status_code, 200)
        self.assertEquals(self.home_response.status_code, 200)

        # templates tests
        self.assertTemplateUsed(self.home_response,'home.html')
        self.assertTemplateUsed(self.blog_response,'blog.html')

        # other tsets
        # pass
