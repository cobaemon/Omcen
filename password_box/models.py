import uuid as uuid_lib
from pathlib import Path

from Crypto.Cipher import AES
from django.db import models
from django.utils.translation import gettext_lazy as _

from config.public_key import Rsa
from config.settings import KEYS_DIR
from omcen.models import OmcenUser


class PasswordBoxUser(models.Model):
    class Meta:
        verbose_name = _('パスワードボックスユーザー')
        verbose_name_plural = _('パスワードボックスユーザー')

    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    omcen_user = models.ForeignKey(
        OmcenUser,
        on_delete=models.CASCADE
    )
    rsa = Rsa(
        Path(KEYS_DIR, 'secret_code.bin'),
        Path(KEYS_DIR, 'rsa_key.pem')
    )
    public_key = rsa.public_key()
    aes_generation_key = models.BinaryField(
        max_length=256,
        default=rsa.encryption(AES.get_random_bytes(32), public_key),
        editable=False,
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


class PasswordBox(models.Model):
    class Meta:
        verbose_name = _('パスワードボックス')
        verbose_name_plural = _('パスワードボックス')
        constraints = [
            models.UniqueConstraint(
                fields=['password_box_user', 'box_name'],
                name="box_name_unique"
            ),
        ]

    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    password_box_user = models.ForeignKey(
        PasswordBoxUser,
        on_delete=models.CASCADE
    )
    box_name = models.CharField(
        _('ボックス名'),
        max_length=64,
        blank=True,
        null=True
    )
    user_name = models.BinaryField(
        max_length=128,
        blank=True,
        null=True
    )
    password = models.BinaryField(
        max_length=1024,
        blank=True,
        null=True
    )
    email = models.BinaryField(
        max_length=256,
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


class PasswordBoxTag(models.Model):
    class Meta:
        verbose_name = _('パスワードボックスタグ')
        verbose_name_plural = _('パスワードボックスタグ')

    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    password_box = models.OneToOneField(
        PasswordBox,
        on_delete=models.CASCADE
    )
    user_name_tag = models.BinaryField(
        max_length=16,
        blank=True,
        null=True
    )
    password_tag = models.BinaryField(
        max_length=16,
        blank=True,
        null=True
    )
    email_tag = models.BinaryField(
        max_length=16,
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


class PasswordBoxNonce(models.Model):
    class Meta:
        verbose_name = _('パスワードボックスノンス')
        verbose_name_plural = _('パスワードボックスノンス')

    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    password_box = models.OneToOneField(
        PasswordBox,
        on_delete=models.CASCADE
    )
    user_name_nonce = models.BinaryField(
        max_length=16,
        blank=True,
        null=True
    )
    password_nonce = models.BinaryField(
        max_length=16,
        blank=True,
        null=True
    )
    email_nonce = models.BinaryField(
        max_length=16,
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
