# -*- coding: utf-8 -*-
"""
Created on 2021/11/09 16:39:37

@author: cobalt
"""
from django.urls import path

from file_encryption.views import Top

app_name = 'File Encryption'

urlpatterns = [
    path('top', Top.as_view(), name='top'),
]
