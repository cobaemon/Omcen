from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView

from omcen.forms import SearchService, CreateServiceForm, ServiceRegistrationForm
from omcen.models import Service, Plan, ServiceGroup, ServiceInUse, OmcenUser


# サービス管理画面
class ServiceControl(LoginRequiredMixin, ListView):
    template_name = 'omcen/service_control.html'
    model = ServiceGroup
    paginate_by = 30
    ordering = 'is_active'
    form = None

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'))
            return self.handle_no_permission()
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        form = SearchService(self.request.GET or None)
        query_set = super().get_queryset()

        if form.is_bound:
            if form.is_valid():
                service_name = form.cleaned_data.get('service_name')

                if service_name:
                    query_set = query_set.filter(service__service_name__icontains=service_name)

            if not query_set.exists():
                messages.info(self.request, '該当するサービスがありませんでした。', extra_tags='info')

        return query_set.order_by('service__service_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchService()

        return context


# サービスの新規作成
class CreateService(LoginRequiredMixin, CreateView):
    template_name = 'omcen/create_service.html'
    model = ServiceGroup
    form_class = CreateServiceForm
    success_url = reverse_lazy('omcen:service_control')

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'))
            return self.handle_no_permission()
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        # サービスを追加する場合、最低でも1つプランをセットする
        with transaction.atomic():
            service = Service.objects.create(service_name=form.cleaned_data['service_name'])
            plan = Plan.objects.create(service=service,
                                       plan_name=form.cleaned_data['plan_name'],
                                       price=form.cleaned_data['price'])

        if all([service, plan]):
            form.instance.service = service
            form.instance.plan = plan
            form.instance.is_active = False

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_success_url(self):
        messages.success(self.request, 'サービスを新しく追加しました。', extra_tags='success')

        return super().get_success_url()


# サービス一覧
class ServiceList(LoginRequiredMixin, ListView):
    template_name = 'omcen/service_list.html'
    model = Service
    paginate_by = 30
    ordering = 'service_name'
    form = None

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'))
            return self.handle_no_permission()
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        query_set = super().get_queryset()
        query_set = query_set.filter(is_active=True)
        return query_set.order_by('service_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = Service.objects.filter(is_active=True)

        services_dict = {}
        for service in services:
            services_dict.update({
                service.service_name: f'{service.service_name}:top'
            })
        context['service_dict'] = services_dict
        return context


# プラン選択画面
class PlanSelection(LoginRequiredMixin, ListView):
    template_name = 'omcen/plan_selection.html'
    model = Plan
    paginate_by = 30
    ordering = 'is_active'
    form = None

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'))
            return self.handle_no_permission()
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        query_set = super().get_queryset()
        query_set = query_set.filter(
            service__service_name=self.request.resolver_match.kwargs['service_name'],
            is_active=True
        )
        return query_set.order_by('plan_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan = Plan.objects.filter(
            service__service_name=self.request.resolver_match.kwargs['service_name'],
            is_active=True
        )
        plan_list = []
        for p in plan:
            plan_list.append([p.plan_name, p.price])
        context['plan_list'] = plan_list
        context['service_name'] = self.request.resolver_match.kwargs['service_name']
        return context


# サービス登録
class ServiceRegistration(LoginRequiredMixin, CreateView):
    template_name = 'omcen/service_registration.html'
    model = ServiceInUse
    form_class = ServiceRegistrationForm

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'))
            return self.handle_no_permission()
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.omcen_user = get_object_or_404(
            OmcenUser,
            username=self.request.user
        )
        form.instance.omcen_service = get_object_or_404(
            ServiceGroup,
            service__service_name=self.request.resolver_match.kwargs['service_name'],
            plan__plan_name=self.request.resolver_match.kwargs['plan_name']
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_name'] = self.request.resolver_match.kwargs['service_name']
        context['plan_name'] = self.request.resolver_match.kwargs['plan_name']
        context['price'] = Plan.objects.get(
            service__service_name=self.request.resolver_match.kwargs['service_name'],
            plan_name=self.request.resolver_match.kwargs['plan_name']
        ).price
        return context

    def get_success_url(self):
        self.success_url = reverse_lazy(f'{self.request.resolver_match.kwargs["service_name"]}:top')
        messages.success(self.request, _('登録が完了しました。'), extra_tags='success')

        return super().get_success_url()
