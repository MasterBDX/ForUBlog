from django.shortcuts import (render,
                              get_object_or_404,
                              redirect)

from django.views import generic
from django.db.models import Q
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from .forms import AddPostForm,AddCategoryForm
from .models import Post, Author, Category

from comments.forms import CommentForm

from main.mixins import AuthorRequiredMixin, AuthorCheckMixin
from main.models import (AboutBlog, AboutMe, PrivacyPolicy)

from urllib.parse import quote_plus


def posts_list_view(request):
    page = request.GET.get('page', 1)
    page_var = 'page'
    blog_var = True
    cates_num = Post.objects.categories_count()
    recent_posts = Post.objects.latest().select_related(
        'author__user').prefetch_related('comments')
    page_qy = Post.objects.qs_paginator(page=page)
    context = {

        'page_var': page_var,
        'page_obj': page_qy,
        'recent_posts': recent_posts,
        'cates_num': cates_num,
        'blog_var': blog_var,
    }
    return render(request, 'posts/list.html', context)


def post_detail(request, slug):
    comments_list_url = reverse('comments-api:list',kwargs={'slug':slug})
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
                   'comments_list_url':comments_list_url,
                   'form': form, 'cates_num': cates_num,
                   'previous': previous_post, 'next': next_post,
                   'share_str': share_str, 'share_title': share_title,}

        return render(request, 'posts/detail.html', context)

    raise Http404()


def category_post_view(request, cat_slug):
    page = request.GET.get('page', 1)
    page_var = 'page'
    filter = Q(categories__slug__icontains=cat_slug)
    cat = get_object_or_404(Category,slug=cat_slug)
    cat_posts = Post.objects.qs_paginator(page=page, filters=filter)
    

    context = {
        'page_obj': cat_posts,
        'page_var': page_var,
        'cat_name':cat.title

    }

    return render(request, 'posts/list.html', context)


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
    return render(request, 'posts/list.html', context)


class AddPostView(LoginRequiredMixin, AuthorRequiredMixin, generic.CreateView):
    template_name = 'posts/create.html'
    form_class = AddPostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        author = Author.objects.filter(user=user).first()
        self.object.author = author
        self.object.save()
        return super().form_valid(form)


class EditPostView(LoginRequiredMixin, AuthorRequiredMixin, AuthorCheckMixin, generic.UpdateView):
    template_name = 'posts/create.html'
    model = Post
    form_class = AddPostForm
    slug_url_kwarg = 'post_slug'


class DeletePostView(LoginRequiredMixin, AuthorRequiredMixin, AuthorCheckMixin, generic.DeleteView):
    template_name = 'posts/confirm_delete.html'
    model = Post
    slug_url_kwarg = 'post_slug'
    success_url = reverse_lazy('blog')


class AddCategoryView(LoginRequiredMixin, AuthorRequiredMixin, generic.CreateView):
    queryset = Category.objects.all()
    form_class = AddCategoryForm
    template_name = 'posts/create_category.html'
    success_url = reverse_lazy('main:categories-dashboard')


class EditCategoryView(LoginRequiredMixin, AuthorRequiredMixin, generic.UpdateView):
    queryset = Category.objects.all()
    form_class = AddCategoryForm
    template_name = 'posts/create_category.html'
    success_url = reverse_lazy('main:categories-dashboard')
