from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from django.utils.timesince import timesince
from django.urls import reverse

from comments.models import Comment,Reply

class ReplySerializer(serializers.ModelSerializer):
    parent = SerializerMethodField()
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
                  'edit_url','delete_url','parent'
                ]
    
    def get_parent(self,obj):
        return obj.comment.id

    def get_owner(self,obj):
        return True
    
    def get_username(self,obj):
        return obj.user.username
    
    def get_timesince(self,obj):
        return timesince(obj.timestamp)
    
    def get_image_url(self,obj):
        try:
            image = obj.user.profileimage.image.url
        except:
            image = '/static/img/default.png'
        return image
    
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
    replies_info = SerializerMethodField()
    add_reply_url = SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
                  'id','post','content','username',
                  'owner','timesince','image_url',
                  'edit_url','delete_url','replies_info',
                  'add_reply_url',
                ]
    
    def get_owner(self,obj):
        return True
    
    def get_username(self,obj):
        return obj.user.username
    
    def get_timesince(self,obj):
        return timesince(obj.timestamp)
    
    def get_image_url(self,obj):
        try:
            image = obj.user.profileimage.image.url
        except:
            image = '/static/img/default.png'
        return image
    
    def get_edit_url(self,obj):
        url = reverse('comments-api:edit',kwargs={'slug':obj.post.slug,
                                                    'pk':obj.pk})
        return url
    
    def get_delete_url(self,obj):
        url = reverse('comments-api:delete',kwargs={'slug':obj.post.slug,
                                                    'pk':obj.pk})
        return url
    
    def get_replies_info(self,obj):
        return {,'url':reverse('comments-api:reply-list',kwargs={
                    'slug':obj.post.slug,
                    'pk':obj.id})}


    def get_add_reply_url(self,obj):
        url = reverse('comments-api:reply-add',kwargs={'slug':obj.post.slug,
                                             'pk':obj.id})
        return url


class CommentAddSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['content']
    

class ReplyAddSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = ['content']
    


    