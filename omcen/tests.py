from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse_lazy

from omcen.factory import OmcenUserFactory
from omcen.views import ServiceList


class ServiceListTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse_lazy('omcen:service_list'))

        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()

        self.omcen_user = OmcenUserFactory

    # ログインしていない状態でサービス一覧画面にアクセスした場合
    def test_dispatch_login_required_mixin_false(self):
        self.request.user = AnonymousUser()
        response = ServiceList.as_view()(self.request)
        self.assertEquals(response.status_code, 302)

    # ログインした状態でサービス一覧画面にアクセスした場合
    def test_dispatch_login_required_mixin_true(self):
        self.request.user = self.omcen_user
        response = ServiceList.as_view()(self.request)
        self.assertEquals(response.status_code, 200)


class PlanSelectionTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(
            reverse_lazy('omcen:plan_selection', kwargs={'service_name': 'Password Box'}))

        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()

        self.omcen_user = OmcenUserFactory

    # ログインしていない状態でプラン選択画面にアクセスした場合
    def test_dispatch_login_required_mixin_false(self):
        self.request.user = AnonymousUser()
        response = ServiceList.as_view()(self.request)
        self.assertEquals(response.status_code, 302)

    # ログインした状態でプラン選択画面にアクセスした場合
    def test_dispatch_login_required_mixin_true(self):
        self.request.user = self.omcen_user
        response = ServiceList.as_view()(self.request)
        self.assertEquals(response.status_code, 200)
