from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.TextInput())
    subject = forms.CharField(widget=forms.TextInput())
    message = forms.CharField(widget=forms.Textarea())
