from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField, AuthenticationForm)
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import EmailActivation, ProfileImage
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
import os

User = get_user_model()


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email ", widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=("Password "),
        strip=False,
        widget=forms.PasswordInput,
    )
    remember_me = forms.BooleanField(required=False, label='Remember me')

    def clean(self):
        email = self.cleaned_data['username']

        qs = User.objects.filter(email=email)
        if qs.exists():
            is_activate = qs.first().is_active
            if not is_activate:
                email_confirm = EmailActivation.objects.filter(email=email)
                confimable_email = email_confirm.confirmable().exists()
                email_exists = EmailActivation.objects.email_exists(email)
                if confimable_email:
                    path_link = reverse('account:email-resend-activation')
                    msg1 = '''your account is inactive, Please check your email to activate your account !
                            <br>
                          to <a href="{link}"> resend 
                                     activation email</a> '''.format(link=path_link)
                    raise forms.ValidationError(mark_safe(msg1))

                elif email_exists:
                    path_link = reverse('account:email-resend-activation')
                    msg2 = ''' your account is still inactive.<br>
                             do you want to <a href="{link}"> resend 
                             activation link to your email ? </a> '''.format(link=path_link)
                    raise forms.ValidationError(mark_safe(msg2))

                raise forms.ValidationError('This user is inactive')

        super().clean()


class MyPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if not qs.exists():
            raise forms.ValidationError('This email is not found ')
        return email


class EmailReActivationForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse('account:register')
            msg = ''' Your Email Does not exists,
                       would you like to <a href="{link}">
                       register </a>'''.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        else:
            if qs.first().user.is_active:
                raise forms.ValidationError(
                    'your email has already been confirmed')
        return email


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password Confirmation', widget=forms.PasswordInput)
    subscribed = forms.BooleanField(
        label='Subscribe to Newsletter', initial=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'username']

    def clean_password2(self):
        data = self.cleaned_data
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 != password2:
            raise forms.ValidationError(" Passwords don't match ")
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('email is already used')
        return email

    def save(self, commit=True):
        data = self.cleaned_data
        password = data.get('password1')
        user = super().save(commit=False)
        user.set_password(password)
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def clean_password(self):
        return self.initial["password"]


class UserProfileForm(forms.ModelForm):
    subscribed = forms.BooleanField(label='Subscribe to Newsletter',
                                    required=False)

    class Meta:
        model = User
        fields = ['username', 'subscribed', ]


class ProfileImageForm(forms.ModelForm):
    x = forms.FloatField(
        required=False, widget=forms.HiddenInput(attrs={'id': 'id_x'}))
    y = forms.FloatField(
        required=False, widget=forms.HiddenInput(attrs={'id': 'id_y'}))
    width = forms.FloatField(
        required=False, widget=forms.HiddenInput(attrs={'id': 'id_height'}))
    height = forms.FloatField(
        required=False, widget=forms.HiddenInput(attrs={'id': 'id_width'}))
    image = forms.ImageField(label='Profile Picture', required=False,
                             widget=forms.ClearableFileInput(attrs={'id': 'id_file'}))

    class Meta:
        model = ProfileImage
        fields = ('image',)

    def clean_image(self):
        image_field = self.cleaned_data.get('image')
        x = self.data.get('x')
        y = self.data.get('y')
        w = self.data.get('width')
        h = self.data.get('height')

        if (image_field == False and self.instance.image):
            self.instance.image.delete(True)

        else:
            if(x and y and w and h):
                def checker(str_num):
                    try:
                        return float(str_num)
                    except:
                        return float(100)

                dim = list(map(lambda x: checker(x), [x, y, w, h]))

                try:
                    image_file = BytesIO(image_field.file.read())
                    image = Image.open(image_file)
                    cropped_image = image.crop(
                        (dim[0], dim[1], dim[2] + dim[0], dim[3] + dim[1]))
                    resized_image = cropped_image.resize(
                        (300, 300), Image.ANTIALIAS)
                    image_file = BytesIO()
                    resized_image.save(image_file, 'PNG')
                    image_field.file = image_file
                    image_field.image = image
                    return image_field

                except IOError:
                    logger.exception("Error during resize image")

            return image_field
