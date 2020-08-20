from django.http import JsonResponse
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from comments.forms import CommentForm, EditCommentForm, ReplyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.safestring import mark_safe

from posts.models import Post
from comments.models import Comment, Reply


COMMENT_MESSAGE = ''' 
    <p>
            Sorry You have to be logged in to be able to add comment please login
    </p>  

    '''

SUCCESS_ADDCOMMENT_MESSAGE = 'Your comment has been added '
SUCCESS_EDITCOMMENT_MESSAGE = 'Your comment has been modified'
SUCCESS_DELETECOMMENT_MESSAGE = 'Your comment has been deleted'

SUCCESS_ADDREPLY_MESSAGE = 'Your reply has been added '
SUCCESS_EDITREPLY_MESSAGE = 'Your reply has been modified'
SUCCESS_DELETEREPLY_MESSAGE = 'Your reply has been deleted'


@login_required
def add_comment_view(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.instance
            comment.user = request.user
            comment.post = post
            form.save()
            messages.success(request, SUCCESS_ADDCOMMENT_MESSAGE)
            return redirect(post.get_absolute_url()+'#postComments')
    return redirect(post.get_absolute_url())


@login_required
def edit_comment_view(request, post_slug, comment_pk):
    user = request.user
    comment = get_object_or_404(Comment,
                                id=comment_pk,
                                user=user)
    if request.method == 'POST':
        edit_form = EditCommentForm(request.POST)
        if edit_form.is_valid():
            content = edit_form.instance.content
            comment.content = content
            comment.save()
            url = comment.post.get_absolute_url() + '#' + str(comment.id)
            messages.success(request, SUCCESS_EDITCOMMENT_MESSAGE)
            return redirect(url)
    return redirect(comment.post.get_absolute_url())


@login_required
def delete_comment_view(request, post_slug, comment_pk):
    user = request.user
    comment = get_object_or_404(Comment,
                                id=comment_pk,
                                user=user,
                                post__slug=post_slug)
    comment.delete()
    messages.success(request, SUCCESS_DELETECOMMENT_MESSAGE)
    return redirect(comment.post.get_absolute_url())


@login_required
def add_reply_view(request, post_slug, comment_pk):
    user = request.user
    post = get_object_or_404(Post, slug=post_slug)
    comment = get_object_or_404(Comment,
                                id=comment_pk,
                                post__slug=post_slug)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.instance
            reply.user = user
            reply.post = post
            reply.comment = comment
            form.save()
            messages.success(request, SUCCESS_ADDREPLY_MESSAGE)
            return redirect(post.get_absolute_url()+'#'+str(reply.comment.id))
    return redirect(post.get_absolute_url())


@login_required
def edit_reply_view(request, post_slug, comment_pk, reply_pk):
    user = request.user
    reply = get_object_or_404(Reply,
                              id=reply_pk,
                              comment__id=comment_pk,
                              user=user,
                              post__slug=post_slug)

    if request.method == 'POST':
        edit_form = ReplyForm(request.POST)
        if edit_form.is_valid():
            content = edit_form.instance.content
            reply.content = content
            reply.save()
            url = reply.post.get_absolute_url() + '#' + str(reply.comment.id)
            messages.success(request, SUCCESS_EDITREPLY_MESSAGE)
            return redirect(url)
    return redirect(reply.post.get_absolute_url())


@login_required
def delete_reply_view(request, post_slug, comment_pk, reply_pk):
    user = request.user
    reply = get_object_or_404(Reply,
                              id=reply_pk,
                              comment__id=comment_pk,
                              user=user,
                              post__slug=post_slug)
    reply.delete()
    messages.success(request, SUCCESS_DELETEREPLY_MESSAGE)
    return redirect(reply.post.get_absolute_url()+'#' + str(reply.comment.id))
