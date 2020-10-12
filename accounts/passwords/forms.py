from django import forms
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class MyPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }


class MyPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if not qs.exists():
            raise forms.ValidationError(_('This email is not found '))
        else:
            obj = qs.first()
            if not obj.is_active:
                raise forms.ValidationError(_('This email is not active yet '))
        return email