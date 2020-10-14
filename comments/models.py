from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from posts.models import Post

User = get_user_model()

class CommentManager(models.Manager):
	def all_real(self):
		return self.get_queryset()

class Comment(models.Model):
    user = models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE,
                            null=True,blank=True)
    post = models.ForeignKey(Post,related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return str(self.user.username)

    objects = CommentManager()

class Reply(models.Model):
    user = models.ForeignKey(User,related_name='replies',on_delete=models.CASCADE,
                            null=True,blank=True)
    post = models.ForeignKey(Post,related_name='replies', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,related_name='replies',on_delete=models.CASCADE) 
    content = models.TextField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')

    def __str__(self):
        return str(self.user.username)

    objects = CommentManager()