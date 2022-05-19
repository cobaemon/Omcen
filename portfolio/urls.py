# -*- coding: utf-8 -*-

from django.urls import path

from portfolio.views import Top, Profile, Deliverables, VocabularyNotebook

app_name = 'Portfolio'

urlpatterns = [
    path('top/', Top.as_view(), name='top'),
    path('profile/', Profile.as_view(), name='profile'),
    path('deliverables/', Deliverables.as_view(), name='deliverables'),
    path('vocabulary_notebook/', VocabularyNotebook.as_view(), name='vocabulary_notebook'),
]
