from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve

from .models import User
from .views import (UserLoginView, UserLogoutView,
                    UserRegistrerView, ProfileView, DeleteUserView)

from .forms import (LoginForm, RegistrationForm, UserProfileForm)


class TestUserUrls(SimpleTestCase):

    def test_authentications_urls(self):
        ''' test authentication urls to test if
            the url have a right view i thin !!! '''

        login_url = reverse('accounts:login')
        logout_url = reverse('accounts:logout')
        register_url = reverse('accounts:register')
        profile_url = reverse('accounts:profile', kwargs={
                              'user_slug': 'omarbd'})
        delete_url = reverse('accounts:delete', kwargs={
                             'user_slug': 'abdullah3'})
        self.assertEquals(resolve(login_url).func.view_class, UserLoginView)
        self.assertEquals(resolve(logout_url).func.view_class, UserLogoutView)
        self.assertEquals(
            resolve(register_url).func.view_class, UserRegistrerView)
        self.assertEquals(resolve(profile_url).func.view_class, ProfileView)
        self.assertEquals(resolve(delete_url).func.view_class, DeleteUserView)


class TestUserViews(TestCase):
    def setUp(self):
        ''' setup the user & client & urls & responses  '''

        self.user = User.objects.create_superuser(email='testbd1@gmail.com',
                                                  username='testbd1',
                                                  password='12345%$#@!',
                                                  subscribed=True
                                                  )

        self.client = Client()
        self.client2 = Client()
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.register_url = reverse('accounts:register')
        self.profile_url = reverse('accounts:profile', kwargs={
                                   'user_slug': 'testbd1'})
        self.delete_url = reverse('accounts:delete', kwargs={
                                  'user_slug': 'testbd1'})

        self.login_response = self.client.get(self.login_url)
        self.logout_response = self.client.get(self.logout_url)
        self.register_response = self.client.get(self.register_url)
        self.profile_response2 = self.client2.get(self.profile_url)

    def test_authentication_templates(self):
        ''' test Authentication templates test
            if the response have a right template '''

        self.client.login(email='testbd1@gmail.com', password='12345%$#@!')
        self.profile_response = self.client.get(self.profile_url)

        self.assertTemplateUsed(self.login_response,
                                'authentication/login.html')
        self.assertTemplateUsed(self.register_response,
                                'authentication/register.html')
        self.assertTemplateUsed(self.profile_response,
                                'authentication/profile.html')

    def test_authentication_response(self):
        ''' test authentication responses to check
            if the response status have the right status '''

        self.client.login(email='testbd1@gmail.com', password='12345%$#@!')
        self.profile_response = self.client.get(self.profile_url)
        self.delete_get_response = self.client.get(self.delete_url)
        self.delete_post_response = self.client.post(self.delete_url)

        self.assertEquals(self.login_response.status_code, 200)
        self.assertEquals(self.register_response.status_code, 200)
        self.assertEquals(self.profile_response.status_code, 200)
        self.assertEquals(self.profile_response2.status_code, 302)
        self.assertEquals(self.logout_response.status_code, 302)
        self.assertEquals(self.delete_get_response.status_code, 200)
        self.assertEquals(self.delete_post_response.status_code, 302)


class TestAccountsModels(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='omarbd6@gmail.com',
                                        username='omarbd6',
                                        )
        self.user.set_password('12345%$#@!')
        self.user.save()

        self.user2 = User.objects.create_user(
            email='omarbd7@gmail.com',
            username='omarbd6',
            password='12345%$#@!'
        )
        self.profile_url = (reverse('accounts:profile', kwargs={
                            'user_slug': self.user2.slug}))
        self.user2_absolute_url = self.user2.get_absolute_url()

    def test_user_model(self):
        self.assertIsNotNone(self.user.slug)
        self.assertNotEquals(self.user.slug, self.user2.slug)
        self.assertIn(self.user.username, self.user.slug)
        self.assertIn('{}-'.format(self.user2.username), self.user2.slug)
        self.assertFalse(self.user2.is_admin)
        self.assertFalse(self.user2.is_staff)
        self.assertFalse(self.user2.is_auther)
        self.assertTrue(self.user2.is_active)
        self.assertEquals(self.profile_url, self.user2_absolute_url)


class TestAuthenticationForms(TestCase):
    def test_register_form(self):
        form = RegistrationForm(data={'email': 'omarbd@gmail.com',
                                      'username': 'omarbd',
                                      'password1': '12345%$#@!',
                                      'password2': '12345%$#@!',
                                      'subscribed': True})
        self.assertTrue(form.is_valid())
