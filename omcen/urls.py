from django.urls import path

from omcen.views import ServiceControl, CreateService, ServiceList, ServiceSubscribe, PlanSelection, ServiceInUseList, \
    ServiceUnsubscribe

app_name = 'omcen'

urlpatterns = [
    # 管理画面
    path('admin/service_control', ServiceControl.as_view(), name='service_control'),
    path('admin/create_service', CreateService.as_view(), name='create_service'),
    # path('admin/update_service/<int:pk>', , name='update_service'),
    # path('admin/delete_service/<int:pk>', , name='delete_service'),
    path('service_list', ServiceList.as_view(), name='service_list'),
    path('<str:service_name>/plan_selection', PlanSelection.as_view(), name='plan_selection'),
    path('<uuid:pk>/service_subscribe', ServiceSubscribe.as_view(), name='service_subscribe'),
    path('<uuid:pk>/service_unsubscribe', ServiceUnsubscribe.as_view(), name='service_unsubscribe'),
    path('service_in_use_list', ServiceInUseList.as_view(), name='service_in_use_list')
]
