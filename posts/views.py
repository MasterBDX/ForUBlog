from django.shortcuts import (render,
                              get_object_or_404,
                              redirect)

from django.views import generic
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from posts.mixins import AuthorRequiredMixin, AuthorCheckMixin
from .forms import AddPostForm
from comments.forms import CommentForm, EditCommentForm, ReplyForm
from .models import Post, Author, Category
from urllib.parse import quote_plus
from myadmin.models import (AboutBlog, AboutMe, PrivacyPolicy)


def post_detail(request, slug):
    qs = Post.objects.filter(slug=slug).select_related(
        'author__user__profileimage').prefetch_related('comments', 'categories')
    user = request.user
    if qs.count() == 1:
        post = qs.first()
        if post.active or user.is_admin or user.is_author:
            form = CommentForm()
            recent_posts = Post.objects.latest().select_related(
                'author__user').prefetch_related('comments')
            cates_num = Post.objects.categories_count()

            share_str = quote_plus(post.overview[:70] + '... ')
            share_title = quote_plus(post.title)

            try:
                previous_post = post.get_previous_by_timestamp()
            except:
                previous_post = None
            try:
                next_post = post.get_next_by_timestamp()
            except:
                next_post = None

        context = {'obj': post, 'recent_posts': recent_posts,
                   'form': form, 'cates_num': cates_num,
                   'previous': previous_post, 'next': next_post,
                   'share_str': share_str, 'editform': EditCommentForm(),
                   'share_title': share_title, 'replyform': ReplyForm()}

        return render(request, 'post/post.html', context)

    raise Http404()


def category_post_view(request, cat_slug):
    page = request.GET.get('page', 1)
    page_var = 'page'
    filter = Q(categories__slug__icontains=cat_slug)
    cat_posts = Post.objects.qs_paginator(page=page, filters=filter)

    context = {
        'page_obj': cat_posts,
        'page_var': page_var,

    }

    return render(request, 'blog.html', context)


def authors_post_view(request, auth_slug):
    author = get_object_or_404(Author, user__slug=auth_slug)

    page = request.GET.get('page', 1)
    page_var = 'page'
    filter = Q(author=author)
    auth_posts = Post.objects.qs_paginator(page=page, filters=filter)

    context = {
        'page_obj': auth_posts,
        'page_var': page_var,
    }
    return render(request, 'blog.html', context)


class AddPostView(LoginRequiredMixin, AuthorRequiredMixin, generic.CreateView):
    template_name = 'post/create_post.html'
    form_class = AddPostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        author = Author.objects.filter(user=user).first()
        self.object.author = author
        self.object.save()
        return super().form_valid(form)


class EditPostView(LoginRequiredMixin, AuthorRequiredMixin, AuthorCheckMixin, generic.UpdateView):
    template_name = 'post/create_post.html'
    model = Post
    form_class = AddPostForm
    slug_url_kwarg = 'post_slug'


class DeletePostView(LoginRequiredMixin, AuthorRequiredMixin, AuthorCheckMixin, generic.DeleteView):
    template_name = 'post/post_confirm_delete.html'
    model = Post
    slug_url_kwarg = 'post_slug'
    success_url = reverse_lazy('blog')


class Dashboard(LoginRequiredMixin, AuthorRequiredMixin, generic.ListView):
    template_name = 'post/dashboard.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        author = self.request.user.author
        qs = super().get_queryset().filter(author=author).order_by('slug')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cates'] = Category.objects.all()
        context['about_me'] = AboutMe.objects.all()
        context['about_blog'] = AboutBlog.objects.all()
        context['privacy_policy'] = PrivacyPolicy.objects.all()
        return context


class AddCategoryView(LoginRequiredMixin, AuthorRequiredMixin, generic.CreateView):
    template_name = 'post/create_category.html'
    model = Category
    fields = ['title']
    success_url = reverse_lazy('posts:dashboard')


class EditCategoryView(LoginRequiredMixin, AuthorRequiredMixin, generic.UpdateView):
    template_name = 'post/create_category.html'
    model = Category
    fields = ['title']
    success_url = reverse_lazy('posts:dashboard')
