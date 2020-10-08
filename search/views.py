import datetime

from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView

from posts.models import Post
from posts.utils import date_capture
from accounts.models import User


def search_posts_view(request):
    # vars
    page_var = 'page'
    page = request.GET.get(page_var, 1)
    q = request.GET.get('q', '0')
    date, exists = date_capture(q)

    if exists:
        year, month, day = date.split('-')

        if int(year) == 0 or int(month) == 0 and int(day) == 0:
            date = '2000-12-12'
    else:
        date = '2000-12-12'

    filters = Q(title__icontains=q) | Q(content__icontains=q) | Q(
        timestamp=date) | Q(author__user__username__icontains=q)
    page_qy = Post.objects.qs_paginator(page=page, filters=filters)

    context = {
        'page_var': page_var,
        'page_obj': page_qy,
    }
    return render(request, 'posts/list.html', context)


class SearchUserView(ListView):
    template_name = 'main/authors_admin.html'
    paginate_by = 20
    page_kwarg = 'page'

    def get_queryset(self):
        q = self.request.GET.get('q', '0')
        if q.isdigit():
            qd = int(q)
        else:
            qd = 0
        filters = Q(username__icontains=q) | Q(
            email__icontains=q) | Q(slug__iexact=q) | Q(id__exact=qd)
        qs = User.objects.filter(filters).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_var'] = 'page'
        return context
