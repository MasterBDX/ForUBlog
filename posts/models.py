from django.db import models
from django.db.models import Count
from django.db.models.signals import pre_save, post_save
from django.contrib.auth import get_user_model
from tinymce import HTMLField
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.safestring import mark_safe

from .utils import (unique_slug_generator,
                    thumbnail_random_name,
                    pro_pic_random_name,
                    )


User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('posts:author_posts', kwargs={'auth_slug': self.user.slug})


class TitleField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(null=True, blank=True)
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:category_posts', kwargs={'cat_slug': self.slug})


class PostManger(models.Manager):

    def all_active(self):
        qs = self.get_queryset().filter(active=True)
        return qs

    def featured(self):
        qs = self.all_active().filter(featured=True)
        return qs

    def latest(self):
        qs = self.all_active()[:3]
        return qs

    def qs_paginator(self, page=1, filters=None):
        if filters:
            posts = self.all_active().filter(filters).select_related('author__user__profileimage',
                                                                     'author__user').prefetch_related('comments', 'categories')
        else:
            posts = self.all_active().select_related('author__user__profileimage',
                                                     'author__user').prefetch_related('comments', 'categories')

        paginator = Paginator(posts, 4)

        try:
            page_qy = paginator.page(page)
        except PageNotAnInteger:
            page_qy = paginator.page(1)
        except EmptyPage:
            page_qy = paginator.page(paginator.num_pages)
        return page_qy

    def categories_count(self):
        qs = self.all_active().order_by('categories').values('categories__title',
                                                             'categories__slug').annotate(cat_num=Count('categories__title'))
        return qs


class Post(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True, null=True)
    content = HTMLField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    author = models.ForeignKey(
        Author, related_name='author', on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=thumbnail_random_name,
                                  null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='categories')
    featured = models.BooleanField(default=False)
    notification = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    objects = PostManger()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def safe_content(self):
        return mark_safe(self.content)

    @property
    def all_comments(self):
        return self.comments.order_by('-timestamp')

    @property
    def comments_count(self):
        return self.comments.order_by('-timestamp').count()


def slug_conf_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_conf_receiver, sender=Post)
