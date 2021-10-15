from django import forms


class SearchService(forms.Form):
    service_name = forms.CharField(label='サービス名', max_length=32, required=False)

    def clean_service_name(self):
        service_name = self.cleaned_data['service_name']

        return service_name
