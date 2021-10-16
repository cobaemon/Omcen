from django.urls import path
from omcen.views import ServiceControl

app_name = 'omcen'

urlpatterns = [
    path('admin/service_control', ServiceControl.as_view(), name='service_control'),
]
