from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import CustomAuthenticationForm, CustomPasswordResetForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
import logging

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        logger.info(f"Successful login for user: {user.email} (ID: {user.id})")
        login(self.request, user)  # Manually log in the user
        if user.must_reset_password:
            logger.info(f"User {user.email} redirected to password change - must_reset_password=True")
            return redirect('users:password_change')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        logger.warning(f"Failed login attempt for username: {form.data.get('username', 'unknown')}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')

    def form_valid(self, form):
        logger.info(f"Password change completed for user: {self.request.user.email} (ID: {self.request.user.id})")
        response = super().form_valid(form)
        self.request.user.must_reset_password = False  # Update must_reset_password to False
        self.request.user.save()  # Save the updated user object
        logger.info(f"must_reset_password flag cleared for user: {self.request.user.email}")
        update_session_auth_hash(self.request, form.user)  # Prevents the user from being logged out
        return response


@method_decorator(csrf_protect, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'users/password_reset_email.txt'
    html_email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "If an account exists with the email you entered, you will receive password reset instructions shortly."
    
    def form_valid(self, form):
        logger.info(f"Password reset form submitted for email: {form.cleaned_data.get('email')}")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        logger.warning(f"Invalid password reset form submission: {form.errors}")
        return super().form_invalid(form)


@method_decorator(csrf_protect, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')
    
    def form_valid(self, form):
        logger.info(f"Password reset confirmation completed for user: {form.user.email} (ID: {form.user.id})")
        # Clear must_reset_password flag when password is reset via email
        form.user.must_reset_password = False
        form.user.save()
        logger.info(f"must_reset_password flag cleared for user: {form.user.email} via password reset")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        logger.warning(f"Invalid password reset confirmation form: {form.errors}")
        return super().form_invalid(form)
