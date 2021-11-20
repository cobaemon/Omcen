# -*- coding: utf-8 -*-
"""
Created on 2021/11/09 16:21:04

@author: cobalt
"""
from django import forms


# ボックス新規作成フォーム
class TopForm(forms.Form):
    file = forms.FileField(
        required=True
    )
