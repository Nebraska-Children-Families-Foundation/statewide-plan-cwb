from django.shortcuts import redirect
from django.urls import reverse


class CheckPasswordResetMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.must_reset_password:
            if request.path not in [reverse('password_change'), reverse('password_change_done')]:
                return redirect('password_change')
        response = self.get_response(request)
        return response
