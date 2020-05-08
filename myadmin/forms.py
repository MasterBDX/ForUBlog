from django import forms

from .models import AboutMe, AboutBlog, PrivacyPolicy


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
