import logging
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.shortcuts import redirect
from django.urls import reverse


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        logging.info(f'User {user.email} must reset password: {user.must_reset_password}')
        if user.must_reset_password:
            logging.info('Redirecting to password change')
            self.request.session['reset_password_user_id'] = user.id
            return redirect('users:password_change')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logging.debug(f'Login view context: {context}')
        return context
