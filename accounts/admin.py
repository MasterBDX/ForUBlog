from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from .models import EmailActivation, ProfileImage
from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'slug', 'is_admin')

    list_filter = ('is_admin',)

    fieldsets = (
        ('User Info', {'fields': ('email', 'username', 'slug', 'password')}),

        ('Permissions', {'fields': ('is_active', 'is_staff',
                                    'is_admin','is_author',
                                    'subscribed', 'check_subscribe')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'subscribed')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(ProfileImage)
admin.site.register(EmailActivation)
admin.site.register(Permission)
