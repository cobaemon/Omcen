# -*- coding: utf-8 -*-

from django import forms
from django.core import validators
from django.utils.translation import gettext_lazy as _


# 文字フィールドバリエーション
class CharFieldValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = '有効な値を入力してください。この値には、数字・文字 @/./+/-/_ のみを含めることができます。'
    flags = 0


# メッセージ送信用フォーム
class EmailForm(forms.Form):
    email_title_validator = CharFieldValidator()
    email_title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'style': 'width:100%',
            'placeholder': _('件名')
        }),
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[email_title_validator],
    )

    email_message_validator = CharFieldValidator()
    email_message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'style': 'width:100%',
            'placeholder': _('内容')
        }),
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[email_message_validator],
    )
