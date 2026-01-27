from django.urls import include, path, re_path
from django.contrib import admin
from core.views import redirect_landing

urlpatterns = [
    # Admin remains accessible
    path('admin/', admin.site.urls),

    # Catch-all: redirect all other traffic to the retirement landing page
    re_path(r'^.*$', redirect_landing, name='redirect_landing'),
]

admin.site.site_header = 'Statewide Plan Admin Panel'
admin.site.site_title = 'Statewide Plan Admin Panel'
