from django.shortcuts import render
from django.views.generic import View
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
User = get_user_model()

from .utils import MailChimp
from .mixins import CsrfExemptMixin
from marketing.models import MarketingPrefrence

class WebHookMailChimp(CsrfExemptMixin,View):
    def get(self ,request,*args,**kwargs):
        return HttpResponse('hello guys',200)

    def post(self ,request,*args,**kwargs ):
        data = dict(request.POST)
        list_id = data.get("data[list_id]")
        
        if list_id:
            if str(list_id[0]) == str(settings.MAILCHIMP_EMAIL_LIST_ID):
                email = data["data[email]"][0]
                json_data,status_code = MailChimp().get_list_member(email)
                list_member_status = json_data['status']
                subscribed,check_subscribe = (None,None)
                if list_member_status == 'subscribed':
                    subscribed,check_subscribe = (True,True)
                elif list_member_status == 'unsubscribed':
                    subscribed,check_subscribe = (False,False)
                if subscribed != None  and check_subscribe != None:
                    qs = User.objects.filter(email=email)
                    if qs.exists() and qs.count()==1:
                        mailchimp_qs = MarketingPrefrence.objects.filter(user=qs.first())
                        qs.update(subscribed=subscribed,
                                  check_subscribe=check_subscribe,
                                  )
                        if mailchimp_qs.exists():
                            mailchimp_qs.update(mailchimp_msg=str(data))
        return HttpResponse('Thank You ',200)    


