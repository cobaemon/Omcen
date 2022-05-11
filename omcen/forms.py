import sys

from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from omcen.models import ServiceGroup, Service, ServiceInUse, OmcenUser, Plan, LinkedID, \
    LinkingOmcenUsersToSocialAccounts

sys.path.append('../templates')


#  管理画面: サービス検索
class SearchService(forms.Form):
    service_name = forms.CharField(label='サービス名', max_length=32, required=False)


# 管理画面: サービス作成フォーム
class CreateServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceGroup
        fields = []

    service_name = forms.CharField(label='サービス名', max_length=32, required=True, help_text="最大文字数は32文字です。")
    plan_name = forms.CharField(label='プラン名', max_length=32, required=True, help_text='最大文字数は32文字です。')
    price = forms.IntegerField(label='価格', required=True)

    def clean_service_name(self):
        if self.cleaned_data['service_name']:
            if Service.objects.filter(service_name=self.cleaned_data['service_name']).exists():
                raise forms.ValidationError('同じサービス名が存在します。')

        return self.cleaned_data['service_name']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError('0より大きい値を入力してください。')

        return self.cleaned_data.get('price')


class CreatePlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['plan_name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError('0より大きい値を入力してください。')

        return self.cleaned_data.get('price')


class UpdatePlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['plan_name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError('0より大きい値を入力してください。')

        return self.cleaned_data.get('price')


class DeletePlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = []


# サービス登録フォーム
class ServiceSubscribeForm(forms.ModelForm):
    class Meta:
        model = ServiceInUse
        fields = []


# サービス登録解除フォーム
class ServiceUnsubscribeForm(forms.ModelForm):
    class Meta:
        model = ServiceInUse
        fields = []


# Omcenユーザー停止フォーム
class OmcenUserDeactivateForm(forms.ModelForm):
    class Meta:
        model = OmcenUser
        fields = []


# プロフィール編集フォーム
class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = OmcenUser
        fields = ['username', 'first_name', 'last_name', 'email']

    username_validator = UnicodeUsernameValidator()
    username = forms.CharField(
        label=_('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        required=True,
        widget=forms.TextInput(attrs={
            'style': 'width:100%',
            'placeholder': _('username')
        }),
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'width:100%',
            'placeholder': _('firstname')
        }),
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'width:100%',
            'placeholder': _('lastname')
        }),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={
            'style': 'width:100%',
            'placeholder': _('email')
        }),
    )


# 連携ID生成フォーム
class LinkedIDPublishingForm(forms.ModelForm):
    class Meta:
        model = LinkedID
        fields = []


# User連携
class LinkingUserForm(forms.ModelForm):
    class Meta:
        model = LinkingOmcenUsersToSocialAccounts
        fields = []

    linked_id = forms.CharField(
        required=True,
        max_length=36,
        widget=forms.TextInput(attrs={
            'style': 'width:100%',
            'placeholder': _('連携ID')
        }),
    )
