from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import ModelChoiceField, Select
from .models import AppUser, CommunityCollaborative, SystemPartner


class AppUserAdmin(BaseUserAdmin):
    model = AppUser
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'start_date')}),
        ('Associations', {'fields': ('community_collaborative', 'system_partner')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        ('Associations', {'fields': ('community_collaborative', 'system_partner')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'community_collaborative', 'system_partner')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    formfield_overrides = {
        # Ensuring the community_collaborative and system_partner use the Select widget
        AppUser.community_collaborative.field: {'widget': Select()},
        AppUser.system_partner.field: {'widget': Select()},
    }


admin.site.register(AppUser, AppUserAdmin)
