from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from django.utils.translation import ugettext as _
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
        print(self.context)
        return obj.comment.id

    def get_owner(self,obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            if obj.user == user:
                return True
        return False
    
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
        url = reverse('comments-api:reply-edit',kwargs={'slug':obj.post.slug,
                                                   'pk':obj.comment.id,
                                                   'reply_id':obj.id})
        return url
    
    def get_delete_url(self,obj):
        url = reverse('comments-api:reply-delete',kwargs={'slug':obj.post.slug,
                                                   'pk':obj.comment.id,
                                                   'reply_id':obj.id})
        return url



class CommentSerialzer(serializers.ModelSerializer):
    owner = SerializerMethodField()
    username = SerializerMethodField()
    timesince = SerializerMethodField()
    image_url = SerializerMethodField()
    edit_url = SerializerMethodField()
    delete_url = SerializerMethodField()
    add_reply_url = SerializerMethodField()
    replies = SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
                  'id','post','content','username',
                  'owner','timesince','image_url',
                  'edit_url','delete_url',
                  'replies','add_reply_url',
                ]
    
    def get_owner(self,obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            if obj.user == user:
                return True
        return False
    
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
    
    def get_replies(self,obj):
        context = self.context
        return ReplySerializer(obj.replies.all(),many=True,
                                context=context).data
    
    def get_add_reply_url(self,obj):
        return reverse('comments-api:reply-add',
                        kwargs={'slug':obj.post.slug,'pk':obj.id})


class CommentAddSerialzer(serializers.ModelSerializer):


    def validate_content(self,value):
        if not value.strip():
            raise serializers.ValidationError(_('This field should not be left blank'))
        return value

    class Meta:
        model = Comment
        fields = ['content']
    

class ReplyAddSerialzer(serializers.ModelSerializer):

    def validate_content(self,value):
        if not value.strip():
            raise serializers.ValidationError(_('This field should not be left blank'))
        return value
    class Meta:
        model = Reply
        fields = ['content']
    


    