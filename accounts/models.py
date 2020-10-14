from django.conf import settings
from django.urls import reverse
from django.db import models
from django.core.mail import send_mail
from django.template.loader import get_template
from django.core.mail import send_mail
from django.contrib.auth.models import (
    AbstractBaseUser, AbstractUser)
from django.utils.translation import gettext_lazy as _

from main.models import BlogInfo
from .managers import (UserManager, EmailActivationManager)
from .utils import (get_propic_name,

                    unique_key_generator)

from PIL import Image


class User(AbstractUser):
    email = models.EmailField(verbose_name='email address',
                              max_length=255, unique=True)
    username = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True)

    subscribed = models.BooleanField(default=True)
    check_subscribe = models.NullBooleanField(blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_shortname(self):
        return self.username

    def get_fullname(self):
        return self.usernaem

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'user_slug': self.slug})

    def notification(self, link):
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
        to_email = [self.email]
        context = {'name': self.username,
                   'link': link}
        txt_ = get_template(
            'authentication/snippets/message.txt').render(context)
        html_ = get_template(
            'authentication/snippets/html_message.html').render(context)

        email = send_mail(
            'New Post',
            txt_,
            from_email,
            to_email,
            html_message=html_,
            fail_silently=False
        )
        return email > 0

    @property
    def is_author(self):
        try:
            if self.author:
                return True
        except self.__class__.author.RelatedObjectDoesNotExist:
            return False
        except:
            raise ValueError('there is some problem')


class EmailActivation(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    email = models.EmailField(max_length=120,
                              blank=True,
                              null=True)
    key = models.CharField(max_length=200, blank=True,
                           null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    class Meta:
        verbose_name = _('Email Activation')
        verbose_name_plural = _('Email Activations')

    def __str__(self):
        return self.user.username

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_email_activate(self):
        if not self.activated and not self.forced_expired:

            blog_info =BlogInfo.objects.last()
            blog_name = None

            if blog_info:
                blog_name = blog_info.name 

            base_url = getattr(settings,
                               'BASE_URL',
                               'https://masterbdx-blog.herokuapp.com')
            key_path = reverse('account:email-activate',
                               kwargs={'key': self.key})

            path = '{base}{k_path}'.format(base=base_url,
                                           k_path=key_path)
            context = {'path': path,
                       'email': self.email,
                       'name': self.user.username,
                       'blog_name':blog_name}
            txt_ = get_template('registration/verify.txt').render(context)
            html_ = get_template('registration/verify.html').render(context)
            subject = '1-Clicl Email Verification'
            from_email = settings.DEFAULT_FROM_EMAIL
            resipient_list = [self.email]
            sent_mail = send_mail(
                subject,
                txt_,
                from_email,
                resipient_list,
                html_message=html_,
                fail_silently=False
            )
        return sent_mail


class ProfileImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True,
                              null=True,
                              upload_to=get_propic_name)  # default='default.png',

    class Meta:
        verbose_name = _('Profile Image')
        verbose_name_plural = _('Profile Images')

    def __str__(self):
        return self.user.username + ' image'
