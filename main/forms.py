from django import forms
from .models import AboutMe, AboutBlog, PrivacyPolicy

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.TextInput())
    subject = forms.CharField(widget=forms.TextInput())
    message = forms.CharField(widget=forms.Textarea())


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
