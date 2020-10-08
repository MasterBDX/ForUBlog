from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .models import Post,Category

from PIL import Image


# def thumbnail_validation(value):
#     img = Image.open(value)
#     # if img.height != 450 and img.width != 800:
#     return value


class AddPostForm(forms.ModelForm):
    # thumbnail = forms.ImageField(validators=[thumbnail_validation])

    class Meta:
        labels = {'title':_('title'),'overview':_('overview'),
                  'content':_('content'),'thumbnail':_('thumbnail'),
                  'categories':_('categories'),'active':_('active'),
                  'featured':_('featured')}
        model = Post
        fields = ['title', 'overview', 'content',
                  'thumbnail', 'categories', 'active', 'featured']
    

class AddCategoryForm(forms.ModelForm):
    class Meta:
        labels = {'title':_('title')}
        model = Category
        fields = ['title']
