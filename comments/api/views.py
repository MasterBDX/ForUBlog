from rest_framework.generics import (ListAPIView,CreateAPIView,
                                     UpdateAPIView,DestroyAPIView)
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status


from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

# from .mixins import CommentContextMixin
from .permissions import (IsOwner,IsOwnerOrAdmin,
                          SameCommentPost,
                          SameCommentAndPost)
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context        
    

class AddCommentAPIView(APIView):

    def post(self,request,*args,**kwargs):
        content = request.data.get('content')
        post = get_object_or_404(Post,slug=self.kwargs.get('slug'))
        user = request.user
        if user.is_authenticated:
            comment = CommentAddSerialzer(data={'content':content})
            if comment.is_valid() :
                obj = comment.save(post=post,user=user)            
                return Response(CommentSerialzer(obj,context={'request':request}).data)
            return Response(_('This field should not be left blank'),status=status.HTTP_400_BAD_REQUEST)
        return Response(_('You have to be loged in to add comment'),status=status.HTTP_403_FORBIDDEN)


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
        if user.is_authenticated:
            comment = get_object_or_404(Comment,pk=self.kwargs.get('pk'))
            reply = ReplyAddSerialzer(data={'content':content})
            if reply.is_valid() :
                obj = reply.save(comment=comment,post=post,user=user)
                return Response(ReplySerializer(obj,context={'request':request}).data)
            return Response(_('This field should not be left blank'),status=status.HTTP_400_BAD_REQUEST)
        return Response(_('You have to be loged in to add reply'),status=status.HTTP_403_FORBIDDEN)



class EditReplyAPIView(UpdateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplyAddSerialzer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwner,
                          SameCommentAndPost]
    lookup_url_kwarg = 'reply_id'


class DeleteReplyAPIView(DestroyAPIView):
    queryset = Reply.objects.all()
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrAdmin,
                          SameCommentAndPost]
    lookup_url_kwarg = 'reply_id'

    