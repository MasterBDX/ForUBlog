from django.contrib.auth.views import (PasswordChangeView,PasswordResetView)

from .forms import (MyPasswordChangeForm,
                    MyPasswordResetForm)

class MyPasswordChangeView(PasswordChangeView):
    form_class = MyPasswordChangeForm


class MyPasswordResetView(PasswordResetView):
    email_template_name = 'accounts/passwords/password_reset_email.html'
    form_class = MyPasswordResetForm