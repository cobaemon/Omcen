from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
import uuid as uuid_lib
from django.utils.translation import gettext_lazy as _

from django.utils import timezone


class OmcenUsers(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        blank=True,
        null=True
    )
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
        null=True
    )
    email = models.EmailField(
        _('email address'),
        unique=True
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    creation_date = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )
    update_date = models.DateTimeField(
        _('update date'),
        auto_now=True
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = False

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Services(models.Model):
    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    service_name = models.CharField(
        max_length=32,
        unique=True,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    creation_date = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )
    update_date = models.DateTimeField(
        _('update date'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')


class Plans(models.Model):
    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    service_name = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
    )
    plan_name = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    price = models.IntegerField(
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    creation_date = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )
    update_date = models.DateTimeField(
        _('update date'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('plan')
        verbose_name_plural = _('plans')


class OmcenServices(models.Model):
    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    service = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
    )
    plan = models.ForeignKey(
        Plans,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    creation_date = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )
    update_date = models.DateTimeField(
        _('update date'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('omcen service')
        verbose_name_plural = _('omcen services')


class ServiceInUse(models.Model):
    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    omcen_user = models.ForeignKey(
        OmcenUsers,
        on_delete=models.CASCADE
    )
    omcen_service = models.ForeignKey(
        OmcenServices,
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    creation_date = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )
    update_date = models.DateTimeField(
        _('update date'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('service in use')
        verbose_name_plural = _('service in use')
