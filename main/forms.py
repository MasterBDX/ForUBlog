from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import AboutMe, AboutBlog, PrivacyPolicy

class ContactForm(forms.Form):
    name = forms.CharField(label=_('name'),widget=forms.TextInput())
    email = forms.EmailField(label=_('email'),widget=forms.TextInput())
    subject = forms.CharField(label=_('subject'),widget=forms.TextInput())
    message = forms.CharField(label=_('message'),widget=forms.Textarea())

    

class AboutMeForm(forms.ModelForm):
    class Meta:
        model = AboutMe
        fields = ['overview', 'content']


class AboutBlogForm(forms.ModelForm):
    class Meta:
        model = AboutBlog
        fields = ['overview', 'content']


class PrivacyPolicyForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicy
        fields = ['overview', 'content']
