from django.db import models
from django.utils.safestring import mark_safe
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

    def __str__(self):
        return self.name



class MianImage(models.Model):
    image = models.ImageField(upload_to=get_image_name)
    content = HTMLField(blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


    def safe_content(self):
        return mark_safe(self.content)




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
