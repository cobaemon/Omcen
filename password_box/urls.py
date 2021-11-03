# -*- coding: utf-8 -*-
"""
Created on 2021/10/25 10:36:56

@author: cobalt
"""
from django.urls import path

from password_box.views import Top, BoxCreate, BoxView, BoxDelete, BoxUpdate, PasswordGenerate

app_name = 'Password Box'

urlpatterns = [
    path('top', Top.as_view(), name='top'),
    path('<uuid:pk>/view', BoxView.as_view(), name='view'),

    # ボックスCRUD
    path('create', BoxCreate.as_view(), name='create'),
    path('<str:password_type>/<int:password_num>/create', BoxCreate.as_view(), name='create'),
    path('<uuid:pk>/delete', BoxDelete.as_view(), name='delete'),
    path('<uuid:pk>/update', BoxUpdate.as_view(), name='update'),

    # パスワード生成
    path('password generate', PasswordGenerate.as_view(), name='password_generate')
]
