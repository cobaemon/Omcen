from django.urls import path

from omcen.views import ServiceControl, CreateService, ServiceList, ServiceSubscribe, PlanSelection, ServiceInUseList, \
    ServiceUnsubscribe, switching_enabled, ServiceDetail, CreatePlan, UpdatePlan, DeletePlan, OmcenUserDeactivate, \
    MyPage, ChangeProfile


app_name = 'omcen'

urlpatterns = [
    # 管理画面
    path('admin/service_control', ServiceControl.as_view(), name='service_control'),

    # サービスCRUD
    path('admin/service_detail/<uuid:service_id>', ServiceDetail.as_view(), name='service_detail'),
    path('admin/create_service', CreateService.as_view(), name='create_service'),
    # path('admin/update_service/<int:pk>', , name='update_service'),
    # path('admin/delete_service/<int:pk>', , name='delete_service'),

    # プランCRUD
    path('admin/create_plan/<uuid:service_id>', CreatePlan.as_view(), name="create_plan"),
    path('admin/update_plan/<uuid:service_id>/<uuid:pk>', UpdatePlan.as_view(), name="update_plan"),
    path('admin/delete_plan/<uuid:service_id>/<uuid:pk>', DeletePlan.as_view(), name="delete_plan"),

    # サービスの有効無効切り替え
    path('admin/switching_enabled/<uuid:service_id>/<uuid:plan_id>/<str:flag>', switching_enabled, name='switching_enabled'),

    path('service_list', ServiceList.as_view(), name='service_list'),
    path('<str:service_name>/plan_selection', PlanSelection.as_view(), name='plan_selection'),
    path('<uuid:pk>/service_subscribe', ServiceSubscribe.as_view(), name='service_subscribe'),
    path('<uuid:pk>/service_unsubscribe', ServiceUnsubscribe.as_view(), name='service_unsubscribe'),
    path('service_in_use_list', ServiceInUseList.as_view(), name='service_in_use_list'),
    path('<uuid:pk>/omcen_user_deactivate', OmcenUserDeactivate.as_view(), name='omcen_user_deactivate'),
    path('my_page', MyPage.as_view(), name='my_page'),
    path('my_page/<uuid:pk>/change_profile', ChangeProfile.as_view(), name='change_profile')
]
