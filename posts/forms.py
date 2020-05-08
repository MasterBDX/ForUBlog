from django import forms
from django.conf import settings
from .models import Post

from PIL import Image


def thumbnail_validation(value):
    img = Image.open(value)
    # if img.height != 450 and img.width != 800:
    return value


class AddPostForm(forms.ModelForm):
    thumbnail = forms.ImageField(validators=[thumbnail_validation])

    class Meta:
        model = Post
        fields = ['title', 'overview', 'content',
                  'thumbnail', 'categories', 'active', 'featured']
