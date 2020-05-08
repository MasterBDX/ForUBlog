from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView, FormView, ListView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm
from posts.models import Post, Author, Category
from myadmin.models import AboutMe, AboutBlog, PrivacyPolicy


def home_page_view(request):
    about_blog = AboutBlog.objects.all().last()
    featured_posts = Post.objects.featured()[:3].select_related('author__user',
                                                                'author__user__profileimage')
    latest_posts = Post.objects.latest().prefetch_related('categories',)
    context = {'featured_posts': featured_posts,
               'latest_posts': latest_posts,
               'about_blog': about_blog,
               }
    return render(request, 'home.html', context)


def blog_view(request):
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
    return render(request, 'blog.html', context)


class AboutMeView(ListView):
    template_name = 'info/about_me.html'

    context_object_name = 'privacy'

    def get_queryset(self):
        qs = AboutMe.objects.all().last()
        return qs


class AboutBlogView(ListView):
    template_name = 'info/about_blog.html'

    context_object_name = 'about_blog'

    def get_queryset(self):
        qs = AboutBlog.objects.all().last()
        return qs


class PrivacyPolicyView(ListView):
    template_name = 'info/privacy_policy.html'
    context_object_name = 'privacy'

    def get_queryset(self):
        qs = PrivacyPolicy.objects.all().last()
        return qs


class ContactMeView(FormView):
    form_class = ContactForm
    template_name = 'info/contact_me.html'
    success_url = reverse_lazy('contact_me')

    def form_valid(self, form):
        subject = form.cleaned_data.get('name')
        from_email = form.cleaned_data.get('email')
        to_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
        message = form.cleaned_data.get('message')
        context = {'name': subject, 'email': to_email, 'message': message, }
        txt_ = get_template('snippets/message.txt').render(context)
        html_ = get_template(
            'snippets/html_message.html').render(context)
        send_mail(
            subject,
            txt_,
            from_email,
            [to_email, ],
            html_message=html_,
            fail_silently=False
        )
        messages.add_message(self.request, messages.SUCCESS,
                             'your message has been sent')
        return redirect('contact_me')
