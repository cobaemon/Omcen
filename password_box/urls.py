# -*- coding: utf-8 -*-
"""
Created on 2021/10/25 10:36:56

@author: cobalt
"""
from django.urls import path

from password_box.views import Top

app_name = 'password_box'

urlpatterns = [
    path('top', Top.as_view(), name='top')
]
