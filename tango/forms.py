# -*- coding: utf-8 -*-
"""
Created on 2021/11/17 7:20:24

@author: cobalt
"""

from django import forms
from django.core import validators
from django.utils.translation import gettext_lazy as _

from tango.models import VocabularyNotebook, Tango


# 文字フィールドバリエーション
class CharFieldValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = '有効な値を入力してください。この値には、数字・文字 @/./+/-/_ のみを含めることができます。'
    flags = 0


# 単語帳CRUD
class VocabularyNotebookCreateForm(forms.ModelForm):
    class Meta:
        model = VocabularyNotebook
        fields = ['vocabulary_notebook_name']

    vocabulary_notebook_name_validator = CharFieldValidator()
    vocabulary_notebook_name = forms.CharField(
        required=True,
        validators=[vocabulary_notebook_name_validator],
        widget=forms.TextInput(attrs={
            'style': 'width:100%',
            'placeholder': _('単語帳名'),
        })
    )


class VocabularyNotebookUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.base_fields['vocabulary_notebook_name'].initial = kwargs.pop('vocabulary_notebook_name')

        super(VocabularyNotebookUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = VocabularyNotebook
        fields = ['vocabulary_notebook_name']

    vocabulary_notebook_name_validator = CharFieldValidator()
    vocabulary_notebook_name = forms.CharField(
        required=True,
        validators=[vocabulary_notebook_name_validator],
        widget=forms.TextInput(attrs={
            'style': 'width:100%',
            'placeholder': _('単語帳名'),
        })
    )

    def clean_vocabulary_notebook_name(self):
        if self.cleaned_data['vocabulary_notebook_name']:
            if VocabularyNotebook.objects.filter(
                    vocabulary_notebook_name=self.cleaned_data['vocabulary_notebook_name']).exists():
                raise forms.ValidationError('同じ単語帳名が存在します。')

        return self.cleaned_data['vocabulary_notebook_name']


# 単語CRUD
class TangoCreateForm(forms.ModelForm):
    class Meta:
        model = Tango
        fields = ['tango', 'contents']

    tango_validator = CharFieldValidator()
    tango = forms.CharField(
        required=True,
        validators=[tango_validator],
        widget=forms.TextInput(attrs={
            'style': 'width:100%',
            'placeholder': _('単語')
        })
    )
    contents = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'style': 'width:100%',
            'placeholder': _('内容'),
            'rows': '10',
        })
    )


class TangoUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.base_fields['tango'].initial = kwargs.pop('tango')
        self.base_fields['contents'].initial = kwargs.pop('contents')

        super(TangoUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Tango
        fields = ['tango', 'contents']

    tango_validator = CharFieldValidator()
    tango = forms.CharField(
        required=True,
        validators=[tango_validator],
        widget=forms.TextInput(attrs={
            'style': 'width:100%',
            'placeholder': _('単語')
        })
    )
    contents = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'style': 'width:100%',
            'placeholder': _('内容'),
            'rows': '10',
        })
    )


# 単語帳検索
class VocabularyNotebookSearchForm(forms.Form):
    vocabulary_notebook_validator = CharFieldValidator()
    vocabulary_notebook_name = forms.CharField(
        validators=[vocabulary_notebook_validator],
        widget=forms.TextInput(attrs={
            'style': 'width:75%',
            'placeholder': _('単語帳名'),
        }),
        required=False
    )
    search_type = forms.fields.ChoiceField(
        choices=(
            ('0', '部分一致'),
            ('1', '完全一致'),
        ),
        required=False
    )


# 単語検索
class TangoSearchForm(forms.Form):
    tango_validator = CharFieldValidator()
    tango = forms.CharField(
        validators=[tango_validator],
        widget=forms.TextInput(attrs={
            'style': 'width:50%',
            'placeholder': _('単語'),
        }),
        required=False
    )
    search_type = forms.fields.ChoiceField(
        choices=(
            ('0', '部分一致'),
            ('1', '完全一致'),
        ),
        required=False
    )
    search_scope = forms.fields.ChoiceField(
        choices=(
            ('0', '単語のみ'),
            ('1', 'すべて'),
        ),
        required=False
    )
