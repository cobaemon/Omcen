# -*- coding: utf-8 -*-
"""
Created on 2021/12/05 13:56:15

@author: cobalt
"""

from django.urls import path

from tango.views import TopView, VocabularyNotebookCreateView, VocabularyNotebookDeleteView, \
    VocabularyNotebookUpdateView, VocabularyNotebookReadView, TangoCreateView, TangoReadView, TangoUpdateView, \
    TangoDeleteView

app_name = 'tango'

urlpatterns = [
    # 単語帳トップページ
    path('top', TopView.as_view(), name='top'),
    # 単語帳CRUD
    path('vocabulary_notebook_create', VocabularyNotebookCreateView.as_view(), name='vocabulary_notebook_create'),
    path('<uuid:pk>/vocabulary_notebook_read', VocabularyNotebookReadView.as_view(), name='vocabulary_notebook_read'),
    path('<uuid:pk>/vocabulary_notebook_update', VocabularyNotebookUpdateView.as_view(),
         name='vocabulary_notebook_update'),
    path('<uuid:pk>/vocabulary_notebook_delete', VocabularyNotebookDeleteView.as_view(),
         name='vocabulary_notebook_delete'),
    # 単語CRUD
    path('<uuid:vocabulary_notebook_pk>/tango/tango_create', TangoCreateView.as_view(), name='tango_create'),
    path('<uuid:vocabulary_notebook_pk>/tango/<uuid:pk>/tango_read', TangoReadView.as_view(), name='tango_read'),
    path('<uuid:vocabulary_notebook_pk>/tango/<uuid:pk>/tango_update', TangoUpdateView.as_view(), name='tango_update'),
    path('<uuid:vocabulary_notebook_pk>/tango/<uuid:pk>/tango_delete', TangoDeleteView.as_view(), name='tango_delete'),
]
