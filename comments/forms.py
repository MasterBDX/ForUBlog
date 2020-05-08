from django import forms
from .models import Comment,Reply


class CommentForm(forms.ModelForm):
    content = forms.CharField(required=False,widget=forms.Textarea(attrs={
    'name':"usercomment",
     'id':"usercomment",
     'placeholder':"Type your comment",
     'class':"form-control",
     'rows':4,
    }))

    class Meta:
        model = Comment
        fields = ['content']

class EditCommentForm(forms.ModelForm):
    content = forms.CharField(label='',
                              required=False,
                              widget=forms.Textarea(attrs={
    'name':"editform",
     'id':"edit-form-field",
     'placeholder':"Type your comment",
     'class':"form-control",
     'rows':3,
    }))

    class Meta:
        model = Comment
        fields = ['content']

class ReplyForm(forms.ModelForm):
    content = forms.CharField(label='Add Reply',required=False,widget=forms.Textarea(attrs={
     'id':"reply-form-field",
     'placeholder':"Type your reply",
     'class':"form-control",
     'rows':3,
    }))

    class Meta:
        model = Reply
        fields = ['content']



