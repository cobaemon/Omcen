import uuid as uuid_lib
from pathlib import Path

from Crypto.Cipher import AES
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import OmcenUser
from config.public_key import Rsa
from config.settings import KEYS_DIR


class FileEncryptionUser(models.Model):
    class Meta:
        verbose_name = _('ファイル暗号化ユーザー')
        verbose_name_plural = _('ファイル暗号化ユーザー')

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
