
from django.db.models.signals import pre_save, post_save
from django.db.models import Q

from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.conf import settings
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.translation import gettext as _


from .models import Category, Post
from .utils import unique_slug_generator

User = get_user_model()


@receiver(pre_save, sender=Category)
def get_cat_slug(instance, sender, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_save, sender=Post)
def slug_conf_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


def notificate(self, link,emails):
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
    to_email = emails
    link = getattr(settings, 'BASE_URL')
    context = {'link': link}
    txt_ = get_template(
        'authentication/snippets/message.txt').render(context)
    html_ = get_template(
        'authentication/snippets/html_message.html').render(context)

    email = send_mail(
        _('New Post'),
        txt_,
        from_email,
        to_email,
        html_message=html_,
        fail_silently=False
    )
    return email > 0

@receiver(pre_save, sender=Post)
def send_notification(sender, instance, **kwargs):
    if instance.active and not instance.notificated:
        link = getattr(settings, 'BASE_URL') + instance.get_absolute_url()
        print(link)
        instance.notificated = True
        users = User.objects.filter(is_active=True,subscribed=True).exclude(Q(is_admin=True) | Q(is_author=True)).values_list('email')
        users = [user[0] for user in users ]

