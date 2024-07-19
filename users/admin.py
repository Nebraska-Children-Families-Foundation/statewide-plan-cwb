from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser


class AppUserAdmin(UserAdmin):
    model = AppUser
    fieldsets = (
        (None, {'fields': ('email', 'password', 'must_reset_password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'start_date')}),
        ('Associations', {'fields': ('community_collaborative', 'system_partner', 'member_type')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'must_reset_password'),
        }),
        ('Roles', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Associations', {'fields': ('member_type', 'community_collaborative', 'system_partner')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'member_type')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    ordering = ('email',)


admin.site.register(AppUser, AppUserAdmin)
