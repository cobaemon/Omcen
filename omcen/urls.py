from django.urls import path

from omcen.views import ServiceControl, CreateService, ServiceList, ServiceSubscribe, PlanSelection, ServiceInUseList, \
    ServiceUnsubscribe, switching_enabled, ServiceDetail, CreatePlan, UpdatePlan, DeletePlan, OmcenUserDeactivate, \
    MyPage, ChangeProfile, LinkingOmcenUsersToSocialAccountsView, LinkedIDPublishing, LinkingUser

app_name = 'Omcen'

urlpatterns = [
    # 管理画面
    path('admin/service_control/', ServiceControl.as_view(), name='service_control'),

    # サービスCRUD
    path('admin/service_detail/<uuid:service_id>/', ServiceDetail.as_view(), name='service_detail'),
    path('admin/create_service', CreateService.as_view(), name='create_service'),
    # path('admin/update_service/<int:pk>', , name='update_service'),
    # path('admin/delete_service/<int:pk>', , name='delete_service'),

    # プランCRUD
    path('admin/create_plan/<uuid:service_id>/', CreatePlan.as_view(), name="create_plan"),
    path('admin/update_plan/<uuid:service_id>/<uuid:pk>/', UpdatePlan.as_view(), name="update_plan"),
    path('admin/delete_plan/<uuid:service_id>/<uuid:pk>/', DeletePlan.as_view(), name="delete_plan"),

    # サービスの有効無効切り替え
    path('admin/switching_enabled/<uuid:service_id>/<uuid:plan_id>/<str:flag>/', switching_enabled,
         name='switching_enabled'),

    # サービス一覧
    path('service_list/', ServiceList.as_view(), name='service_list'),
    # プラン選択
    path('<str:service_name>/plan_selection/', PlanSelection.as_view(), name='plan_selection'),
    # サービス登録
    path('<uuid:pk>/service_subscribe/', ServiceSubscribe.as_view(), name='service_subscribe'),
    # サービス登録解除
    path('<uuid:pk>/service_unsubscribe/', ServiceUnsubscribe.as_view(), name='service_unsubscribe'),
    # 登録中のサービス一覧
    path('service_in_use_list/', ServiceInUseList.as_view(), name='service_in_use_list'),

    # omcenユーザの停止
    path('<uuid:pk>/omcen_user_deactivate/', OmcenUserDeactivate.as_view(), name='omcen_user_deactivate'),
    # マイページ
    path('my_page/', MyPage.as_view(), name='my_page'),
    # プロフィール編集
    path('my_page/<uuid:pk>/change_profile/', ChangeProfile.as_view(), name='change_profile'),
    # 連携ID発行
    path('account_linking/linked_id_publishing/', LinkedIDPublishing.as_view(), name='linked_id_publishing'),
    # ソーシャルアカウントの連携一覧
    path('account_linking/linking_omcen_users_to_social_accounts/', LinkingOmcenUsersToSocialAccountsView.as_view(),
         name='linking_omcen_users_to_social_accounts'),
    # User連携
    path('account_linking/linking_user/', LinkingUser.as_view(), name='linking_user'),
]
