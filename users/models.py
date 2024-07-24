from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from core.plan_actors import CommunityCollaborative, SystemPartner
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('must_reset_password', True)

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
        extra_fields.setdefault('must_reset_password', True)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    class MemberTypes(models.TextChoices):
        COMMUNITY_COLLABORATIVE = 'CC', _('Community Collaborative Member')
        SYSTEM_PARTNER = 'SP', _('System Partner Member')
        NCFF_TEAM = 'NT', _('NCFF Team Member')

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=30, unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True, null=True)
    must_reset_password = models.BooleanField(default=True, help_text=_('Requires user to reset password on next login'))
    start_date = models.DateTimeField(_('start date'), default=timezone.now)
    end_date = models.DateTimeField(_('end date'), blank=True, null=True)

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff member'), default=False)

    community_collaborative = models.ForeignKey(
        CommunityCollaborative,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='users'
    )
    system_partner = models.ForeignKey(
        SystemPartner,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='users'
    )
    member_type = models.CharField(
        max_length=2,
        choices=MemberTypes.choices,
        default=MemberTypes.COMMUNITY_COLLABORATIVE,
        help_text=_('Type of member')
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@receiver(post_save, sender=AppUser)
def reset_password_handler(sender, instance, **kwargs):
    if instance.must_reset_password and not instance.has_usable_password():
        instance.must_reset_password = True
        instance.save()
