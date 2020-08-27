from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from django.utils.timesince import timesince
from django.urls import reverse

from comments.models import Comment,Reply

class ReplaySerializer():
    owner = SerializerMethodField()
    username = SerializerMethodField()
    timesince = SerializerMethodField()
    image_url = SerializerMethodField()
    edit_url = SerializerMethodField()
    delete_url = SerializerMethodField()

    class Meta:
        model = Reply
        fields = [
                  'id','post','content','username',
                  'owner','timesince','image_url',
                  'edit_url','delete_url'
                ]
    
    def get_owner(self,obj):
        return True
    
    def get_username(self,obj):
        return obj.user.username
    
    def get_timesince(self,obj):
        return timesince(obj.timestamp)
    
    def get_image_url(self,obj):
        return obj.user.profileimage.image.url
    
    def get_edit_url(self,obj):
        url = 'google '#reverse('comments-api:edit',kwargs={'slug':obj.post.slug,
              #                                      'pk':obj.pk})
        return url
    
    def get_delete_url(self,obj):
        url = 'faccebook'#reverse('comments-api:delete',kwargs={'slug':obj.post.slug,
               #                                     'pk':obj.pk})
        return url



class CommentSerialzer(serializers.ModelSerializer):
    owner = SerializerMethodField()
    username = SerializerMethodField()
    timesince = SerializerMethodField()
    image_url = SerializerMethodField()
    edit_url = SerializerMethodField()
    delete_url = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
                  'id','post','content','username',
                  'owner','timesince','image_url',
                  'edit_url','delete_url'
                ]
    
    def get_owner(self,obj):
        return True
    
    def get_username(self,obj):
        return obj.user.username
    
    def get_timesince(self,obj):
        return timesince(obj.timestamp)
    
    def get_image_url(self,obj):
        return obj.user.profileimage.image.url
    
    def get_edit_url(self,obj):
        url = reverse('comments-api:edit',kwargs={'slug':obj.post.slug,
                                                    'pk':obj.pk})
        return url
    
    def get_delete_url(self,obj):
        url = reverse('comments-api:delete',kwargs={'slug':obj.post.slug,
                                                    'pk':obj.pk})
        return url


class CommentAddSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['content']
    
    


    