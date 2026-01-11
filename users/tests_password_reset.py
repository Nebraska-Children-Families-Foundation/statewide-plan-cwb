"""
Comprehensive test suite for password reset functionality.
Tests cover security, rate limiting, logging, and user experience.
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail
from django.core.cache import cache
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.messages import get_messages
from unittest.mock import patch
import logging
import time

User = get_user_model()


class PasswordResetFormTest(TestCase):
    """Test custom password reset form functionality."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='oldpassword123'
        )
        self.client = Client()
        # Clear cache before each test
        cache.clear()
    
    def test_form_valid_email(self):
        """Test form with valid email address."""
        response = self.client.post(reverse('users:password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to done page
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Reset your Statewide Plan Portal password', mail.outbox[0].subject)
    
    def test_form_nonexistent_email(self):
        """Test form with non-existent email (should still return success for security)."""
        response = self.client.post(reverse('users:password_reset'), {
            'email': 'nonexistent@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Still redirect
        self.assertEqual(len(mail.outbox), 0)  # No email sent
    
    def test_form_inactive_user(self):
        """Test form with inactive user email (should still return success for security)."""
        self.user.is_active = False
        self.user.save()
        
        response = self.client.post(reverse('users:password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)  # No email sent to inactive user
    
    def test_rate_limiting(self):
        """Test rate limiting prevents abuse."""
        email = 'test@example.com'
        
        # Make 3 requests (should all work)
        for i in range(3):
            response = self.client.post(reverse('users:password_reset'), {
                'email': email
            })
            self.assertEqual(response.status_code, 302)
        
        # 4th request should be rate limited
        response = self.client.post(reverse('users:password_reset'), {
            'email': email
        })
        self.assertEqual(response.status_code, 200)  # Form redisplayed with error
        self.assertContains(response, 'Too many password reset requests')
    
    def test_email_normalization(self):
        """Test email is normalized (lowercase, stripped)."""
        response = self.client.post(reverse('users:password_reset'), {
            'email': '  TEST@EXAMPLE.COM  '
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
    
    def test_invalid_email_format(self):
        """Test invalid email format."""
        response = self.client.post(reverse('users:password_reset'), {
            'email': 'invalid-email'
        })
        self.assertEqual(response.status_code, 200)  # Form redisplayed
        self.assertContains(response, 'Enter a valid email address')


class PasswordResetViewTest(TestCase):
    """Test password reset views."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='oldpassword123'
        )
        self.client = Client()
        cache.clear()
    
    def test_password_reset_form_get(self):
        """Test GET request to password reset form."""
        response = self.client.get(reverse('users:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reset Password')
        self.assertContains(response, 'Having trouble?')
    
    def test_password_reset_done_page(self):
        """Test password reset done page."""
        response = self.client.get(reverse('users:password_reset_done'))
        self.assertEqual(response.status_code, 200)
    
    def test_password_reset_complete_page(self):
        """Test password reset complete page."""
        response = self.client.get(reverse('users:password_reset_complete'))
        self.assertEqual(response.status_code, 200)
    
    def test_password_reset_confirm_valid_token(self):
        """Test password reset confirmation with valid token."""
        # Generate valid token
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        
        # Get the form (first time with token redirects to set-password form)
        response = self.client.get(reverse('users:password_reset_confirm', 
                                         kwargs={'uidb64': uid, 'token': token}))
        # Django redirects from valid token to set-password URL
        self.assertEqual(response.status_code, 302)
        
        # Get the actual form page with set-password token
        response = self.client.get(reverse('users:password_reset_confirm', 
                                         kwargs={'uidb64': uid, 'token': 'set-password'}))
        self.assertEqual(response.status_code, 200)
        
        # Submit new password
        response = self.client.post(reverse('users:password_reset_confirm', 
                                          kwargs={'uidb64': uid, 'token': 'set-password'}), {
            'new_password1': 'newpassword123!',
            'new_password2': 'newpassword123!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to complete
        
        # Verify password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123!'))
        self.assertFalse(self.user.must_reset_password)  # Flag should be cleared
    
    def test_password_reset_confirm_invalid_token(self):
        """Test password reset confirmation with invalid token."""
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        
        response = self.client.get(reverse('users:password_reset_confirm', 
                                         kwargs={'uidb64': uid, 'token': 'invalid-token'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'invalid')


class PasswordResetSecurityTest(TestCase):
    """Test security aspects of password reset."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='oldpassword123',
            must_reset_password=True
        )
        self.client = Client()
        cache.clear()
    
    @patch('users.views.logger')
    def test_security_logging(self, mock_logger):
        """Test that security events are logged."""
        # Test successful password reset request
        self.client.post(reverse('users:password_reset'), {
            'email': 'test@example.com'
        })
        mock_logger.info.assert_called()
        
        # Test failed login logging
        self.client.post(reverse('users:login'), {
            'username': 'test@example.com',
            'password': 'wrongpassword'
        })
        mock_logger.warning.assert_called()
    
    def test_must_reset_password_integration(self):
        """Test integration with must_reset_password system."""
        # User with must_reset_password=True
        self.assertTrue(self.user.must_reset_password)
        
        # Reset password via email should clear the flag
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        
        # First visit the token URL to set the session
        self.client.get(reverse('users:password_reset_confirm', 
                               kwargs={'uidb64': uid, 'token': token}))
        
        # Then submit the new password
        self.client.post(reverse('users:password_reset_confirm', 
                               kwargs={'uidb64': uid, 'token': 'set-password'}), {
            'new_password1': 'newpassword123!',
            'new_password2': 'newpassword123!'
        })
        
        self.user.refresh_from_db()
        self.assertFalse(self.user.must_reset_password)
    
    def test_email_template_security_content(self):
        """Test that email templates contain security warnings."""
        self.client.post(reverse('users:password_reset'), {
            'email': 'test@example.com'
        })
        
        self.assertEqual(len(mail.outbox), 1)
        email_body = mail.outbox[0].body
        
        # Check for security warnings in text email
        self.assertIn('ad blocker', email_body)
        self.assertIn('24 hours', email_body)
        self.assertIn("didn't request", email_body)
        self.assertIn('Never share', email_body)


class PasswordResetIntegrationTest(TestCase):
    """Integration tests for complete password reset workflow."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='oldpassword123'
        )
        self.client = Client()
        cache.clear()
    
    def test_complete_password_reset_workflow(self):
        """Test complete password reset workflow from start to finish."""
        # Step 1: Request password reset
        response = self.client.post(reverse('users:password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)
        
        # Step 2: Check email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, ['test@example.com'])
        
        # Step 3: Extract reset link from email
        self.assertIn('/reset/', email.body)
        
        # Step 4: Simulate clicking reset link (extract token and uid)
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        
        # Step 5: Get reset form (Django redirects valid token to set-password)
        response = self.client.get(reverse('users:password_reset_confirm', 
                                         kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(response.status_code, 302)
        
        # Get the actual form page
        response = self.client.get(reverse('users:password_reset_confirm', 
                                         kwargs={'uidb64': uid, 'token': 'set-password'}))
        self.assertEqual(response.status_code, 200)
        
        # Step 6: Submit new password
        response = self.client.post(reverse('users:password_reset_confirm', 
                                          kwargs={'uidb64': uid, 'token': 'set-password'}), {
            'new_password1': 'newpassword123!',
            'new_password2': 'newpassword123!'
        })
        self.assertEqual(response.status_code, 302)
        
        # Step 7: Verify password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123!'))
        
        # Step 8: Test login with new password
        response = self.client.post(reverse('users:login'), {
            'username': 'test@example.com',
            'password': 'newpassword123!'
        })
        self.assertEqual(response.status_code, 302)  # Successful login redirect
    
    def test_forgot_password_link_on_login(self):
        """Test that login page contains forgot password link."""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Forgot Password?')
        self.assertContains(response, reverse('users:password_reset'))


class PasswordResetTemplateTest(TestCase):
    """Test password reset templates and UI."""
    
    def setUp(self):
        self.client = Client()
    
    def test_password_reset_form_template(self):
        """Test password reset form template content."""
        response = self.client.get(reverse('users:password_reset'))
        self.assertEqual(response.status_code, 200)
        
        # Check for improved UI elements
        self.assertContains(response, 'Having trouble?')
        self.assertContains(response, 'Back to Sign In')
        self.assertContains(response, 'Send Reset Link')
        self.assertContains(response, 'spam folder')
    
    def test_form_validation_display(self):
        """Test that form validation errors are displayed properly."""
        response = self.client.post(reverse('users:password_reset'), {
            'email': 'invalid-email'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'invalid-feedback')
        self.assertContains(response, 'Enter a valid email address')