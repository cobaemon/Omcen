# -*- coding: utf-8 -*-
"""
Created on 2021/10/25 10:36:56

@author: cobalt
"""
from django.urls import path

from password_box.views import Top, BoxCreate, BoxView

app_name = 'Password Box'

urlpatterns = [
    path('top', Top.as_view(), name='top'),
    path('create', BoxCreate.as_view(), name='create'),
    path('<uuid:pk>/view', BoxView.as_view(), name='view')
]
