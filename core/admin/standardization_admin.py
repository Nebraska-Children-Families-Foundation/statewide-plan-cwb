from django.contrib import admin


class ActivityStatusAdmin(admin.ModelAdmin):
    list_display = ('activity_status',)
    search_fields = ('activity_status',)
