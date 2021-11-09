# -*- coding: utf-8 -*-
"""
Created on 2021/10/26 14:58:02

@author: cobalt
"""

from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from password_box.models import PasswordBox


# ボックス新規作成フォーム
class BoxCreateForm(forms.ModelForm):
    class Meta:
        model = PasswordBox
        fields = []

    box_name_validator = UnicodeUsernameValidator()
    box_name = forms.CharField(
        max_length=64,
        validators=[box_name_validator],
        required=True,
    )
    user_name = forms.CharField(
        max_length=128,
        required=False
    )
    password = forms.CharField(
        max_length=1024,
        required=False,
        widget=forms.PasswordInput()
    )
    password_generate_flg = forms.BooleanField(
        label=_('パスワード生成'),
        initial=False,
        required=False
    )
    password_type = forms.fields.ChoiceField(
        choices=(
            ('1', '数字のみ'),
            ('2', '英数字'),
            ('3', '英数字・記号')
        ),
        required=True
    )
    password_num = forms.IntegerField(
        max_value=1024,
        min_value=1,
        required=True,
        initial=16
    )
    email = forms.CharField(
        max_length=256,
        required=False
    )


# ボックス削除フォーム
class BoxDeleteForm(forms.ModelForm):
    class Meta:
        model = PasswordBox
        fields = []


# ボックス編集フォーム
class BoxUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.base_fields['box_name'].initial = kwargs.pop('box_name')
        self.base_fields['user_name'].initial = kwargs.pop('user_name')
        self.base_fields['password'].initial = kwargs.pop('password')
        self.base_fields['email'].initial = kwargs.pop('email')

        super(BoxUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PasswordBox
        fields = []

    box_name_validator = UnicodeUsernameValidator()
    box_name = forms.CharField(
        max_length=64,
        validators=[box_name_validator],
        required=True,
    )
    user_name = forms.CharField(
        max_length=128,
        required=False
    )
    password = forms.CharField(
        max_length=1024,
        widget=forms.PasswordInput(),
        required=False
    )
    email = forms.CharField(
        max_length=256,
        required=False
    )


# パスワード生成
class PasswordGenerateForm(forms.Form):
    password_type = forms.fields.ChoiceField(
        choices=(
            ('1', '数字のみ'),
            ('2', '英数字'),
            ('3', '英数字・記号')
        ),
        required=True
    )
    password_num = forms.IntegerField(
        max_value=1024,
        min_value=1,
        required=True,
        initial=16
    )
