from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


from .models import User, EmailActivation, ProfileImage
from .utils import unique_slug_generator, unique_key_generator
from marketing.models import MarketingPrefrence
from marketing.utils import MailChimp
from posts.models import Author


def get_subscribe_status(instance):
    if instance.subscribed:
        json, status_code = MailChimp().subscribe(email=instance.email)
    else:
        json, status_code = MailChimp().unsubscribe(email=instance.email)

    obj, created = MarketingPrefrence.objects.get_or_create(user=instance)
    obj.mailchimp_msg = json
    obj.save()
    
    if status_code == 200:
        instance.check_subscribe = instance.subscribed
        instance.save()
    return True

@receiver(pre_save, sender=User)
def get_user_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_save, sender=EmailActivation)
def get_email_activation_key(sender, instance, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance.__class__)


@receiver(post_save, sender=User)
def make_email_activation(sender, instance, created, **kwargs):
    profile_image = ProfileImage.objects.get_or_create(user=instance)
    if created:
        if instance.is_admin:
            author, created = Author.objects.get_or_create(user=instance)

        if not instance.is_active:
            obj = EmailActivation.objects.create(
                user=instance, email=instance.email)
            obj.send_email_activate()
        get_subscribe_status(instance)

        # if instance.subscribed:
        #     json, status_code = MailChimp().subscribe(email=instance.email)
        # else:
        #     json, status_code = MailChimp().unsubscribe(email=instance.email)

        # obj, created = MarketingPrefrence.objects.get_or_create(user=instance)
        # obj.mailchimp_msg = json
        # obj.save()
        # instance.check_subscribe = instance.subscribed
        # instance.save()

    else:
        if instance.subscribed != instance.check_subscribe:
            get_subscribe_status(instance)

            # if instance.subscribed:
            #     json, status_code = MailChimp().subscribe(email=instance.email)
            # else:
            #     json, status_code = MailChimp().unsubscribe(email=instance.email)

            # if status_code == 200:
            #     instance.check_subscribe = instance.subscribed
            #     instance.save()

            # obj, created = MarketingPrefrence.objects.get_or_create(
            #     user=instance)
            # obj.mailchimp_msg = json
            # obj.save()
