import uuid as uuid_lib

from allauth.socialaccount.models import SocialAccount
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import OmcenUser


class LinkedID(models.Model):
    class Meta:
        verbose_name = _('連携ID')
        verbose_name_plural = _('連携ID')

    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )

    linked_id = models.UUIDField(
        blank=True,
        null=True
    )
    omcen_user = models.ForeignKey(
        OmcenUser,
        on_delete=models.CASCADE,
    )
    life_span = models.DateTimeField(
        _('life_span'),
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
    )


class LinkingOmcenUsersToSocialAccounts(models.Model):
    class Meta:
        verbose_name = _('ソーシャルアカウントの連携')
        verbose_name_plural = _('ソーシャルアカウントの連携')

    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    omcen_user = models.ForeignKey(
        OmcenUser,
        on_delete=models.CASCADE,
    )
    social_account = models.ForeignKey(
        SocialAccount,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('作成日時'),
        auto_now_add=True
    )


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
    description = models.CharField(
        _('説明'),
        max_length=8192,
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
