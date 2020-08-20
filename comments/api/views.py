from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from .serializers import CommentSerialzer,CommentAddSerialzer
from comments.models import Comment
from posts.models import Post

class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerialzer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        qs = Comment.objects.filter(post__slug=slug)
        
        return qs        
    

class AddCommentAPIView(CreateAPIView):
    serializer_class = CommentAddSerialzer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        post = get_object_or_404(Post,slug=self.kwargs.get('slug'))
        user = self.request.user
        serializer.save(user=user,post=post)