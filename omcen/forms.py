import sys

from django import forms

from omcen.models import ServiceGroup, Service, ServiceInUse, Plan

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


# サービス登録フォーム
class ServiceUnsubscribeForm(forms.ModelForm):
    class Meta:
        model = ServiceInUse
        fields = []
