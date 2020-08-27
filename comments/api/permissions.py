from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    message = 'You must be the owner of the object'
    def has_object_permission(self,request,view,obj):
        pk = view.kwargs.get('pk')
        return obj.user == request.user or \
                   request.user.is_admin
    

class SameCommentPost(BasePermission):
    message = 'comment post must be the same of slug endpoint'

    def has_object_permission(self,request,view,obj):
        slug = view.kwargs.get('slug')
        return obj.post.slug == slug