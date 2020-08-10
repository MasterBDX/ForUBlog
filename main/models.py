from django.db import models
from django.utils.safestring import mark_safe
from tinymce import HTMLField


class AboutMe(models.Model):
    overview = models.TextField(blank=True, null=True)
    content = HTMLField(blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'About Me'

    def safe_content(self):
        return mark_safe(self.content)


class AboutBlog(models.Model):
    overview = models.TextField(blank=True, null=True)
    content = HTMLField(blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'About Blog'

    def safe_content(self):
        return mark_safe(self.content)


class PrivacyPolicy(models.Model):
    overview = models.TextField(blank=True, null=True)
    content = HTMLField(blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Privacy and Policy'

    def safe_content(self):
        return mark_safe(self.content)
