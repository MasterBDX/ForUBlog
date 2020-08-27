from rest_framework.generics import (ListAPIView,CreateAPIView,
                                     UpdateAPIView,DestroyAPIView)
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from django.shortcuts import get_object_or_404


from .permissions import IsOwnerOrAdmin,SameCommentPost
from .pagination import CommentsPagination
from .serializers import CommentSerialzer,CommentAddSerialzer
from comments.models import Comment
from posts.models import Post

class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerialzer
    pagination_class = CommentsPagination
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        qs = Comment.objects.filter(post__slug=slug)
        
        return qs        
    

class AddCommentAPIView(APIView):
    def post(self,request,*args,**kwargs):
        content = request.data.get('content')
        post = get_object_or_404(Post,slug=self.kwargs.get('slug'))
        user = request.user
        comment = CommentAddSerialzer(data={'content':content})
        if comment.is_valid() :
            obj = comment.save(post=post,user=user)
            
        return Response(CommentSerialzer(obj).data)
    


class EditCommentAPIView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentAddSerialzer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrAdmin,
                          SameCommentPost]


class DeleteCommentAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrAdmin,
                          SameCommentPost]