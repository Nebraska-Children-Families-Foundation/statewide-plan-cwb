from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.utils import timezone
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={'autofocus': True}))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email address"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        }),
        help_text=_("Enter the email address associated with your account.")
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            
            # Rate limiting: Check if this email has requested a reset recently
            rate_limit_key = f"password_reset_rate_limit_{email}"
            recent_requests = cache.get(rate_limit_key, 0)
            
            if recent_requests >= 3:  # Max 3 requests per hour
                logger.warning(f"Rate limit exceeded for password reset: {email}")
                raise ValidationError(
                    _("Too many password reset requests. Please wait an hour before trying again."),
                    code='rate_limited'
                )
            
            # Check if user exists (but don't reveal this in error message for security)
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    logger.warning(f"Password reset attempted for inactive user: {email}")
                    # Don't reveal that the account exists but is inactive
                    pass
            except User.DoesNotExist:
                logger.warning(f"Password reset attempted for non-existent email: {email}")
                # Don't reveal that the email doesn't exist for security reasons
                pass
        
        return email
    
    def save(self, domain_override=None, subject_template_name='users/password_reset_subject.txt',
             email_template_name='users/password_reset_email.html', use_https=False,
             token_generator=None, from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        
        email = self.cleaned_data["email"]
        logger.info(f"Password reset requested for email: {email}")
        
        # Increment rate limiting counter
        rate_limit_key = f"password_reset_rate_limit_{email}"
        current_count = cache.get(rate_limit_key, 0)
        cache.set(rate_limit_key, current_count + 1, 3600)  # 1 hour timeout
        
        return super().save(
            domain_override=domain_override,
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            use_https=use_https,
            token_generator=token_generator,
            from_email=from_email,
            request=request,
            html_email_template_name=html_email_template_name,
            extra_email_context=extra_email_context
        )
