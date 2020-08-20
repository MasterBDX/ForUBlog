from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (CreateView, UpdateView,
                                  DeleteView, View)

from django.views.generic.edit import FormMixin
from django.http import Http404
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy, reverse

from .models import User, EmailActivation, ProfileImage

from .forms import (LoginForm, RegistrationForm,
                    UserProfileForm, ProfileImageForm,
                    MyPasswordResetForm, EmailReActivationForm)


class UserRegistrerView(SuccessMessageMixin, CreateView):
    form_class = RegistrationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('account:login')
    success_message = "We sent you the activation link please check your email ."


class EmailActivationView(FormMixin, View):
    success_url = reverse_lazy('account:login')
    form_class = EmailReActivationForm

    def get(self, request, *args, key=None, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(
                    request, 'Your account has been confirmed ; Please login')
                return redirect('account:login')

            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse('password_reset')
                    msg = """ your email has already been confirmed
                            Do you want to <a href="{link}"> reset your password </a> ?

                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect('account:login')
        context = {'form': self.get_form(), 'key': key}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        user.email = email
        user.save()
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_email_activate()
        return super().form_valid(form)

    def form_invalid(self, form):
        request = self.request
        context = {'form': form, 'key': self.key}
        return render(request, 'registration/activation-error.html', context)


class MyPasswordResetView(PasswordResetView):
    form_class = MyPasswordResetForm


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me', None)
        login(self.request, form.get_user())
        if remember_me:
            self.request.session.set_expiry(1209600)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return super().dispatch(request, *args, **kwargs)
        raise Http404


class UserLogoutView(LogoutView):
    next_page = 'accounts:login'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('main:home')
    slug_url_kwarg = 'user_slug'
    template_name = 'authentication/user_confirm_delete.html'

    def get_object(self):
        return self.request.user


@login_required
def profile_view(request, user_slug):
    user = request.user
    user_image, created = ProfileImage.objects.get_or_create(user=user)
    profile_form = UserProfileForm(request.POST or None, instance=user)

    profile_image_form = ProfileImageForm(request.POST or None,
                                          request.FILES or None,
                                          instance=user_image)
    if request.method == 'POST':
        if profile_image_form.is_valid() and profile_form.is_valid():

            obj = profile_form.save()
            image_obj = profile_image_form
            image_obj.save()
            return redirect(user.get_absolute_url())

    context = {'profile_form': profile_form,
               'image_form': profile_image_form}
    return render(request, 'authentication/profile.html', context)
