from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, AbstractUser)

from datetime import timedelta


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None,
                    is_active=True, is_staff=False, is_admin=False, subscribed=True):
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.subscribed = subscribed
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, password=None, subscribed=True):
        user = self.create_user(
            email, username, password=password, is_staff=True, subscribed=subscribed)
        return user

    def create_superuser(self, email, username,
                         password=None, subscribed=True):
        user = self.create_user(email, username, password=password,
                                is_staff=True, is_admin=True, subscribed=subscribed)
        return user

    def qs_paginator(self, page=1, filter=None):
        if filter:
            users = self.get_queryset().filter(filter)
        else:
            users = self.get_queryset()
        users_pagintor = Paginator(users, 10)

        try:
            user_qy = users_pagintor.page(page)
        except PageNotAnInteger:
            user_qy = users_pagintor.page(1)
        except EmptyPage:
            user_qy = users_pagintor.page(users_pagintor.num_pages)

        return user_qy


class EmailActivationQuerySet(models.QuerySet):
    def confirmable(self):
        now = timezone.now()
        default_activation_days = getattr(
            settings, 'DEFAULT_ACTIVATION_DAYS', 7)
        start_range = now - timedelta(days=default_activation_days)
        end_range = now
        return self.filter(activated=False,
                           forced_expired=False,
                           timestamp__range=(start_range, end_range))


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(
            Q(email=email) | Q(user__email=email)).filter(activated=False)
