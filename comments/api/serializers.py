from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from django.utils.timesince import timesince
from comments.models import Comment

class CommentSerialzer(serializers.ModelSerializer):
    owner = SerializerMethodField()
    username = SerializerMethodField()
    timesince = SerializerMethodField()
    image_url = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id','post','content','username','owner','timesince','image_url']
    
    def get_owner(self,obj):
        return True
    
    def get_username(self,obj):
        return obj.user.username
    
    def get_timesince(self,obj):
        return timesince(obj.timestamp)
    
    def get_image_url(self,obj):
        return obj.user.profileimage.image.url
    

class CommentAddSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post','user','content']
    
    


    