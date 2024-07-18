from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={'autofocus': True}))


class PasswordResetForm(SetPasswordForm):
    pass
