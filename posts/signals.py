from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from .models import Category, Post
from django.conf import settings
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


@receiver(pre_save, sender=Category)
def get_cat_slug(instance, sender, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title.lower())


@receiver(pre_save, sender=Post)
def send_notification(sender, instance, **kwargs):
    if instance.active and not instance.notification:
        instance.notification = True
        users = User.objects.filter(subscribed=True).exclude(is_admin=True)
        for user in users:
            if not user.is_author:
                user.notification(settings.BASE_URL +
                                  instance.get_absolute_url())
