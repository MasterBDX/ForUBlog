from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from tinymce import HTMLField

from .utils import get_image_name


class BlogInfo(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    
    facebook = models.URLField(null=True,blank=True)
    twitter = models.URLField(null=True,blank=True)
    instagram = models.URLField(null=True,blank=True)
    
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _('Blog Info')
        verbose_name_plural = _('Blog Info')

    def __str__(self):
        return self.name



class MianImage(models.Model):
    image = models.ImageField(upload_to=get_image_name)
    content = HTMLField(blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _('Mian Image')
        verbose_name_plural = _('Main Images')

    def safe_content(self):
        return mark_safe(self.content)




class AboutMe(models.Model):
    overview = models.TextField(blank=True, null=True)
    content = HTMLField(blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _('About Us')
        verbose_name_plural = _('About Us')

    def safe_content(self):
        return mark_safe(self.content)


class AboutBlog(models.Model):
    overview = models.TextField(blank=True, null=True)
    content = HTMLField(blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _('About Blog')
        verbose_name_plural = _('About Blog')
        

    def safe_content(self):
        return mark_safe(self.content)


class PrivacyPolicy(models.Model):
    overview = models.TextField(blank=True, null=True)
    content = HTMLField(blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _('Privacy and Policy')
        verbose_name_plural = _('Privacy and Policy')

    def safe_content(self):
        return mark_safe(self.content)
