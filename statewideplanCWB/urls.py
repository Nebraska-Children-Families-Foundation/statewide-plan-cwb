from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
]

admin.site.site_header = 'Statewide Plan Admin Panel'
admin.site.site_title = 'Statewide Plan Admin Panel'
