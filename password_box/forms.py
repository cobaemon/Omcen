# -*- coding: utf-8 -*-
"""
Created on 2021/10/26 14:58:02

@author: cobalt
"""

from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator

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
