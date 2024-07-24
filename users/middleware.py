from django.shortcuts import redirect
from django.urls import reverse
import logging

class CheckPasswordResetMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        if request.user.is_authenticated and request.user.must_reset_password:
            self.logger.debug(f'Request path: {request.path}')
            self.logger.debug(f'Password change URL: {reverse("users:password_change")}')
            self.logger.debug(f'Password change done URL: {reverse("users:password_change_done")}')
            if request.path not in [reverse('users:password_change'), reverse('users:password_change_done')]:
                return redirect('users:password_change')
        response = self.get_response(request)
        return response
