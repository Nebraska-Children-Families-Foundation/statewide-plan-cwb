from django.test import TestCase
from users.models import AppUser


class CustomUserManagerTest(TestCase):

    def test_create_user(self):
        user = AppUser.objects.create_user(
            email='normal@user.com',
            password='foo',
            username='normal',
            first_name='Test',
            last_name='User'
        )
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.username, 'normal')
        self.assertTrue(user.check_password('foo'))
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        admin_user = AppUser.objects.create_superuser(
            email='super@user.com',
            password='foo',
            username='admin'
        )
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.username, 'admin')
        self.assertTrue(admin_user.check_password('foo'))
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_active)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            AppUser.objects.create_user(
                email=None,
                password='foo',
                username='user'
            )

    def test_create_user_without_username(self):
        with self.assertRaises(ValueError):
            AppUser.objects.create_user(
                email='user@user.com',
                password='foo',
                username=None
            )

    def test_create_superuser_with_is_superuser_false(self):
        with self.assertRaises(ValueError):
            AppUser.objects.create_superuser(
                email='super@user.com',
                password='foo',
                username='admin',
                is_superuser=False
            )

    def test_create_superuser_with_is_staff_false(self):
        with self.assertRaises(ValueError):
            AppUser.objects.create_superuser(
                email='super@user.com',
                password='foo',
                username='admin',
                is_staff=False
            )
