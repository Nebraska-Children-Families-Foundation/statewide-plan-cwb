from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from .forms import CustomAuthenticationForm


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
