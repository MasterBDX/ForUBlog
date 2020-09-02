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
from .serializers import (CommentSerialzer,CommentAddSerialzer,
                          ReplyAddSerialzer,ReplySerializer)
from comments.models import Comment,Reply
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


class AddReplyAPIView(APIView):
    def post(self,request,*args,**kwargs):
        content = request.data.get('content')
        post = get_object_or_404(Post,slug=self.kwargs.get('slug'))
        user = request.user
        comment = get_object_or_404(Comment,pk=self.kwargs.get('pk'))
        reply = ReplyAddSerialzer(data={'content':content})
        if reply.is_valid() :
            obj = reply.save(comment=comment,post=post,user=user)
        return Response(ReplySerializer(obj).data)


class ReplyListAPIView(ListAPIView):
    serializer_class = ReplySerializer
    pagination_class = CommentsPagination
    
    def get_queryset(self):
        comment_id = self.kwargs.get('pk')
        qs = Reply.objects.filter(comment__id=comment_id)
        return qs