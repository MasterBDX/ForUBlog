from django.shortcuts import render, reverse, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from blog.decorators import super_user_only
from accounts.models import User
from posts.models import Author
from .models import AboutBlog, AboutMe, PrivacyPolicy
from .forms import AboutBlogForm, AboutMeForm, PrivacyPolicyForm
from .mixins import AdminRequiredMixin
import string


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

    return render(request, 'my_admin/authors_admin.html', context)


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
        return redirect('myadmin:authors_admin')
    return render(request, 'my_admin/confirm_author.html', {"status": status, 'username': username})


class AddAboutmeView(AdminRequiredMixin, CreateView):
    form_class = AboutMeForm
    template_name = 'my_admin/info.html'
    success_url = reverse_lazy('posts:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About Me'
        context['process'] = 'Add'
        return context


class AddAboutblogView(AdminRequiredMixin, CreateView):
    form_class = AboutBlogForm
    template_name = 'my_admin/info.html'
    success_url = reverse_lazy('posts:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About Blog'
        context['process'] = 'Add'
        return context


class AddPrvacyPolicyView(AdminRequiredMixin, CreateView):
    form_class = PrivacyPolicyForm
    template_name = 'my_admin/info.html'
    success_url = reverse_lazy('posts:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Privacy & Policy'
        context['process'] = 'Add'
        return context


class EditAboutmeView(AdminRequiredMixin, UpdateView):
    queryset = AboutMe.objects.all()
    form_class = AboutMeForm
    template_name = 'my_admin/info.html'
    success_url = reverse_lazy('posts:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About Me'
        context['process'] = 'Edit'
        return context


class EditAboutblogView(AdminRequiredMixin, UpdateView):
    queryset = AboutBlog.objects.all()
    form_class = AboutBlogForm
    template_name = 'my_admin/info.html'
    success_url = reverse_lazy('posts:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About Blog'
        context['process'] = 'Edit'
        return context


class EditPrvacyPolicyView(AdminRequiredMixin, UpdateView):
    queryset = PrivacyPolicy.objects.all()
    form_class = PrivacyPolicyForm
    template_name = 'my_admin/info.html'
    success_url = reverse_lazy('posts:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Privacy & Policy'
        context['process'] = 'Edit'
        return context


class DeleteAboutmeView(AdminRequiredMixin, DeleteView):
    queryset = AboutMe.objects.all()
    template_name = 'my_admin/delete_confirm.html'
    success_url = reverse_lazy('posts:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About Me'
        return context


class DeleteAboutblogView(AdminRequiredMixin, DeleteView):
    queryset = AboutBlog.objects.all()
    template_name = 'my_admin/delete_confirm.html'
    success_url = reverse_lazy('posts:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About Blog'
        return context


class DeletePrvacyPolicyView(AdminRequiredMixin, DeleteView):
    queryset = PrivacyPolicy.objects.all()
    template_name = 'my_admin/delete_confirm.html'
    success_url = reverse_lazy('posts:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Privacy & Policy'
        return context
