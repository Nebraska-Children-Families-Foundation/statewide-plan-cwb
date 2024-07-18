from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import AppUser


class AppUserAdmin(BaseUserAdmin):
    model = AppUser
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',
                                    'must_reset_password')}),
        ('Important dates', {'fields': ('last_login', 'start_date')}),
        ('Associations', {'fields': ('community_collaborative', 'system_partner', 'member_type')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'must_reset_password'),
        }),
        ('Associations', {'fields': ('community_collaborative', 'system_partner', 'member_type')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'member_type')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(AppUser, AppUserAdmin)
