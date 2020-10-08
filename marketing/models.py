from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save, pre_delete ,post_delete

from .utils import MailChimp

class MarketingPrefrence(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)


    mailchimp_msg = models.TextField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email

# #{{{{============================= Signals ========================}}}

# def make_mark_pref_receiver(sender, instance, created,*args, **kwargs):

#     ''' django check if the user is a new user or already
#         exist depending on that django will be make the mark pref  '''

#     if created:
        
#         if instance.subscribed:
#             json , status_code = MailChimp().subscribe(email=instance.email)
#         else:
#             json , status_code = MailChimp().unsubscribe(email=instance.email)
#         MarketingPrefrence.objects.create(user=instance, mailchimp_msg=json)
#         instance.check_subscribe = instance.subscribed

#     else:
#         if instance.subscribed != instance.check_subscribe:
#             if instance.subscribed:
#                 json, status_code = MailChimp().subscribe(email=instance.email)
#             else:
#                 json , status_code = MailChimp().unsubscribe(email=instance.email)

#             if status_code == 200:
#                 instance.check_subscribe = instance.subscribed
#                 instance.save()

#             obj,created = MarketingPrefrence.objects.get_or_create(user=instance)
#             obj.mailchimp_msg = json
#             obj.save()


# post_save.connect(make_mark_pref_receiver, sender=settings.AUTH_USER_MODEL)

#===========================================================================

def delete_list_member_receiver(sender,instance, using, *args, **kwargs):

    ''' if the user deleted his account signal
        will delete his member in mailchimp '''

    MailChimp().delete_list_member(instance.user.email)
post_delete.connect(delete_list_member_receiver,sender=MarketingPrefrence)
