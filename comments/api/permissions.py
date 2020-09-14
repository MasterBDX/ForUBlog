from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    message = 'You must be the owner of the object'
    def has_object_permission(self,request,view,obj):
        pk = view.kwargs.get('pk')
        return obj.user == request.user or \
                   request.user.is_admin

class IsOwner(BasePermission):
    message = 'You must be the owner of the object'
    def has_object_permission(self,request,view,obj):
        pk = view.kwargs.get('pk')
        return obj.user == request.user
    

class SameCommentPost(BasePermission):
    message = 'comment post must be the same of slug endpoint'

    def has_object_permission(self,request,view,obj):
        slug = view.kwargs.get('slug')
        return obj.post.slug == slug


class SameCommentAndPost(BasePermission):
    message = 'comment pk and post slug must be the same of slug and pk endpoint'

    def has_object_permission(self,request,view,obj):
        slug = view.kwargs.get('slug')
        pk = view.kwargs.get('pk')
        return obj.post.slug == slug and obj.comment.id == pk