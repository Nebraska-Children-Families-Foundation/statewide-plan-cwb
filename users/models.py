from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned to is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password, **extra_fields):
        username = extra_fields.pop('username', None)

        if not email:
            raise ValueError(_('You must provide a valid email address'))
        if not username:
            raise ValueError(_('You must provide a unique username'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=30, unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True, null=True)
    start_date = models.DateTimeField(_('start date'), default=timezone.now())
    end_date = models.DateTimeField(_('end date'), blank=True, null=True)

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff member'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username
