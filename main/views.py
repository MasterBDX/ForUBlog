from django.shortcuts import render, reverse, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.conf import settings

from django.views.generic import (
        TemplateView, FormView, ListView,
        CreateView, UpdateView, DeleteView
        )
from django.views import generic

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.db.models import Q

from .forms import ContactForm

from posts.models import Post, Author, Category
from .models import AboutMe, AboutBlog, PrivacyPolicy,MianImage
from .mixins import AuthorRequiredMixin, AuthorCheckMixin,AdminRequiredMixin
from blog.decorators import super_user_only

from .forms import AboutBlogForm, AboutMeForm, PrivacyPolicyForm
import string


User = get_user_model()

def home_page_view(request):
    main_obj = MianImage.objects.last()
    featured_posts = Post.objects.featured()[:3].select_related('author__user',
                                                                'author__user__profileimage')
    latest_posts = Post.objects.all().prefetch_related('categories',)[:3]
    context = {'featured_posts': featured_posts,
               'latest_posts': latest_posts,
               'obj':main_obj
               
               }
    return render(request, 'main/home.html', context)



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


class ContactUsView(FormView):
    form_class = ContactForm
    template_name = 'info/contact_us.html'
    success_url = reverse_lazy('main:contact_us')

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


class PostsDashboard(LoginRequiredMixin, AuthorRequiredMixin, generic.ListView):
    template_name = 'main/dashboards/posts.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        author = self.request.user.author
        qs = super().get_queryset().filter(author=author).order_by('slug')
        return qs


class CategoriesDashboard(LoginRequiredMixin,generic.ListView):
    template_name = 'main/dashboards/categories.html'
    model = Post
    context_object_name = 'cates'


# class InfoDashboard(LoginRequiredMixin,AdminRequiredMixin,generic.ListView):
#     template_name = 'main/dashboards/info.html'
#     model = AboutBlog
#     context_object_name = 'about_me'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['about_me'] = AboutMe.objects.all()
#         context['privacy_policy'] = PrivacyPolicy.objects.all()
#         return context


@login_required
@super_user_only
def authors_admin_view(request):
    page_var = 'page'
    page = request.GET.get(page_var, 1)
    alpha = list(string.ascii_lowercase)
    beta = request.GET.get('beta')
    if beta:
        filter = Q(username__istartswith=beta)
        current_page = User.objects.qs_paginator(page=page, filter=filter)
    else:
        current_page = User.objects.qs_paginator(page=page)

    context = {'page_obj': current_page,
               'page_var': page_var,
               'alpha': alpha}

    return render(request, 'main/authors_admin.html', context)


@login_required
@super_user_only
def confirm_author_view(request, slug):
    confirm = request.POST.get('confirm')
    status = request.POST.get('status', 'create')
    username = User.objects.filter(slug=slug).values(
        'username').first()['username']

    if confirm:
        user = User.objects.filter(slug=slug).first()
        if user.is_author:
            status = 'deleted'
            author = Author.objects.filter(user__slug=slug).first().delete()
        else:
            status = 'created'
            author = Author.objects.create(user=user)

        messages.add_message(request, messages.SUCCESS,
                             'You have successfuly {} Author for {} '.format(status, username).upper())
        return redirect('main:authors_admin')
    return render(request, 'main/confirm_author.html', {"status": status, 'username': username})


