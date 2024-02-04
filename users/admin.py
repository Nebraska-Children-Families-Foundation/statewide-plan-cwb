from django.contrib import admin
from .models import AppUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class AppUserAdmin(UserAdmin):
    model = AppUser
    search_fields = ['email', 'username', 'first_name', 'last_name']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    ordering = ['username']
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active']

    fieldsets = [
        (None, {'fields': ['email', 'username', 'first_name', 'last_name']}),
        ('Permissions', {'fields': ['is_active', 'is_staff']}),
    ]

    add_fieldsets = [
        (None, {'fields': ['email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff']})
    ]


admin.site.register(AppUser, AppUserAdmin)