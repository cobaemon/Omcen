import uuid as uuid_lib

from django.db import models

from accounts.models import OmcenUser


class VocabularyNotebook(models.Model):
    class Meta:
        verbose_name = '単語帳'
        verbose_name_plural = '単語帳'
        constraints = [
            models.UniqueConstraint(
                fields=['omcen_user', 'vocabulary_notebook_name'],
                name="vocabulary_notebook_unique"
            ),
        ]

    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )

    omcen_user = models.ForeignKey(
        OmcenUser,
        on_delete=models.CASCADE
    )

    vocabulary_notebook_name = models.CharField(
        '単語帳',
        max_length=64,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        '作成日時',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        '更新日時',
        auto_now=True
    )


class Tango(models.Model):
    class Meta:
        verbose_name = '単語'
        verbose_name_plural = '単語'
        constraints = [
            models.UniqueConstraint(
                fields=['vocabulary_notebook', 'tango'],
                name="tango_unique"
            ),
        ]

    uuid = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False
    )
    vocabulary_notebook = models.ForeignKey(
        VocabularyNotebook,
        on_delete=models.CASCADE
    )

    tango = models.CharField(
        '単語',
        max_length=64,
        blank=True,
        null=True
    )
    contents = models.CharField(
        '内容',
        max_length=8192,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        '作成日時',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        '更新日時',
        auto_now=True
    )
