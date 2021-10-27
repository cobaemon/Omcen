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
    user_name = forms.CharField(max_length=128)
    password = forms.CharField(max_length=1024, widget=forms.PasswordInput())
    email = forms.CharField(max_length=256)


# ボックス削除フォーム
class BoxDeleteForm(forms.ModelForm):
    class Meta:
        model = PasswordBox
        fields = []
