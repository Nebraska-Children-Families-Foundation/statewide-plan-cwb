from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import CustomAuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)  # Manually log in the user
        if user.must_reset_password:
            return redirect('users:password_change')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.user.must_reset_password = False  # Update must_reset_password to False
        self.request.user.save()  # Save the updated user object
        update_session_auth_hash(self.request, form.user)  # Prevents the user from being logged out
        return response


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    email_template_name = 'registration/password_reset_email.txt'
    html_email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_message = "If an account exists with the email you entered, you will receive password reset instructions."
