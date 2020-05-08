from django.test import TestCase, SimpleTestCase, Client
from django.urls import resolve , reverse

from .views import authers_admin_view, confirm_auther_view
from accounts.models import User

class TestMyAdminUrls(SimpleTestCase):

    def test_autheradmin_url(self):

        authers_admin_url = reverse('myadmin:authers_admin')
        authers_admin_confirm_url = reverse('myadmin:confirm_auther',kwargs={'slug':'omarbd'})

        self.assertEquals(resolve(authers_admin_url).func, authers_admin_view)
        self.assertEquals(resolve(authers_admin_confirm_url).func,confirm_auther_view)

class TestMyAdminViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(email='testbd1@gmail.com',
                                                  username='testbd1',
                                                  password='12345%$#@!',
                                                  subscribed=True
                                                 )
        self.None_login_client = Client()
        self.login_client = Client()
        self.authers_admin_response_not_login = self.None_login_client.get(reverse("myadmin:authers_admin"))
        self.confirm_auther_response_not_login = self.None_login_client.get(reverse("myadmin:confirm_auther",kwargs={'slug':'testbd1'}))

    def test_my_admin_responses(self):
        self.login_client.login(username='testbd1@gmail.com',password='12345%$#@!')

        self.authers_admin_response_login = self.login_client.get(reverse("myadmin:authers_admin"))
        self.confirm_auther_response_login = self.login_client.get(reverse("myadmin:confirm_auther",kwargs={'slug':'testbd1'}))

        self.assertEquals(self.authers_admin_response_not_login.status_code, 302)
        self.assertEquals(self.confirm_auther_response_not_login.status_code, 302)
        self.assertEquals(self.authers_admin_response_login.status_code, 200)
        self.assertEquals(self.confirm_auther_response_login.status_code, 200)

    def test_my_admin_used_templates(self):
        self.login_client.login(username='testbd1@gmail.com',password='12345%$#@!')

        self.authers_admin_response_login = self.login_client.get(reverse("myadmin:authers_admin"))
        self.confirm_auther_response_login = self.login_client.get(reverse("myadmin:confirm_auther",kwargs={'slug':'testbd1'}))

        self.assertTemplateUsed(self.authers_admin_response_login,'my_admin/authers_admin.html')
        self.assertTemplateUsed(self.confirm_auther_response_login,'my_admin/confirm_auther.html')
