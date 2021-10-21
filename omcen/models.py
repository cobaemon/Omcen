import uuid as uuid_lib

from django.apps import apps
from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class OmcenUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class OmcenUser(AbstractBaseUser, PermissionsMixin):
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

    objects = OmcenUserManager()

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


class Service(models.Model):
    class Meta:
        verbose_name = _('サービス')
        verbose_name_plural = _('サービス')

    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    service_name = models.CharField(
        _('サービス名'),
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
    created_at = models.DateTimeField(
        _('作成日時'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('更新日時'),
        auto_now=True
    )


class Plan(models.Model):
    class Meta:
        verbose_name = _('プラン')
        verbose_name_plural = _('プラン')
     
    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
    )
    plan_name = models.CharField(
        _('プラン名'),
        max_length=32,
        blank=True,
        null=True
    )
    price = models.IntegerField(
        _('価格'),
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
    created_at = models.DateTimeField(
        _('作成日時'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('更新日時'),
        auto_now=True
    )


class ServiceGroup(models.Model):
    class Meta:
        verbose_name = _('サービスグループ')
        verbose_name_plural = _('サービスグループ')

    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
    )
    plan = models.ForeignKey(
        Plan,
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
    created_at = models.DateTimeField(
        _('作成日時'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('更新日時'),
        auto_now=True
    )


class ServiceInUse(models.Model):
    class Meta:
        verbose_name = _('加入中サービス')
        verbose_name_plural = _('加入中サービス')

    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    omcen_user = models.ForeignKey(
        OmcenUser,
        on_delete=models.CASCADE
    )
    omcen_service = models.ForeignKey(
        ServiceGroup,
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
    created_at = models.DateTimeField(
        _('作成日時'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('更新日時'),
        auto_now=True
    )
