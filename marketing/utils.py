from django.conf import settings

import re
import requests
import json
import hashlib

MAILCHIMP_API_KEY = getattr(settings, 'MAILCHIMP_API_KEY')
MAILCHIMP_DATA_CENTER = getattr(settings, 'MAILCHIMP_DATA_CENTER')
MAILCHIMP_EMAIL_LIST_ID = getattr(settings, 'MAILCHIMP_EMAIL_LIST_ID')


def check_email(email):
    if not re.match(r'.+@.+\..+', email):
        raise ValueError(' The string passed not a valid email !')
    return email


def email_hash(email):
    eml = check_email(email).lower().encode()
    em = hashlib.md5(eml)
    return em.hexdigest()


class MailChimp(object):

    def __init__(self):
        self.key = MAILCHIMP_API_KEY
        self.api_url = 'https://{dc}.api.mailchimp.com/3.0'.format(
            dc=MAILCHIMP_DATA_CENTER)
        self.list_id = MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = self.api_url + \
            '/lists/{list_id}/members'.format(list_id=self.list_id)

    def check_valid_status(self, status):
        choices = ['subscribed', 'unsubscribed',
                   'cleaned', 'pending', 'transactional']
        if status not in choices:
            raise ValueError(' Not a valid choice for email status !')
        return status

    def get_email_hash(self, email):
        return email_hash(email)

    def get_list_member(self, email):
        end_url = self.list_endpoint + '/' + self.get_email_hash(email)
        r = requests.get(end_url, auth=('', self.key))
        return r.json(), r.status_code

    def get_list_members(self):
        r = requests.get(self.list_endpoint, auth=('', self.key))
        return r.json(), r.status_code

    def change_list_members_status(self, email, status):
        data = {'email_address': email,
                'status': self.check_valid_status(status)}
        end_url = self.list_endpoint + '/' + self.get_email_hash(email)
        r = requests.put(end_url, auth=('', self.key), data=json.dumps(data))
        return r.json(), r.status_code

    def subscribe(self, email):
        return self.change_list_members_status(email, 'subscribed')

    def unsubscribe(self, email):
        return self.change_list_members_status(email, 'unsubscribed')

    def delete_list_member(self, email):
        end_url = self.list_endpoint + '/' + self.get_email_hash(email)
        r = requests.delete(end_url, auth=('', self.key))
        return r
