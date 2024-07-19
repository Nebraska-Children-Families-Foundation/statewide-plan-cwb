from django.urls import path
from .views import CustomLoginView, PasswordResetView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
]
