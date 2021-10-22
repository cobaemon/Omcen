from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView

from omcen.forms import SearchService, CreateServiceForm, ServiceSubscribeForm, ServiceUnsubscribeForm, \
    OmcenUserDeactivateForm
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
        query_set = super().get_queryset()
        query_set = query_set.filter(
            service__service_name=self.request.resolver_match.kwargs['service_name'],
            is_active=True
        )

        return query_set.order_by('plan__plan_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_in_use'] = ServiceInUse.objects.filter(
            omcen_user__username=self.request.user,
            omcen_service__service__service_name=self.request.resolver_match.kwargs['service_name'],
            is_active=True
        )

        return context


# サービスの登録
class ServiceSubscribe(LoginRequiredMixin, CreateView):
    template_name = 'omcen/service_subscribe.html'
    model = ServiceInUse
    form_class = ServiceSubscribeForm

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'))

            return self.handle_no_permission()

        if ServiceInUse.objects.filter(omcen_user__username=self.request.user,
                                       omcen_service__uuid=self.request.resolver_match.kwargs['pk'],
                                       is_active=True).exists():
            service_in_use = get_object_or_404(
                ServiceInUse,
                omcen_user__username=self.request.user,
                omcen_service__uuid=self.request.resolver_match.kwargs['pk'],
                is_active=True
            )
            return redirect(to=reverse('omcen:service_unsubscribe', kwargs={'pk': service_in_use.uuid}))

        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.omcen_user = self.request.user
        form.instance.omcen_service = get_object_or_404(
            ServiceGroup,
            uuid=self.request.resolver_match.kwargs['pk']
        )
        if ServiceInUse.objects.filter(omcen_user__username=self.request.user,
                                       omcen_service__service__service_name=form.instance.omcen_service.service.service_name,
                                       is_active=True).exists():
            before_service_in_use = ServiceInUse.objects.filter(
                omcen_user__username=self.request.user,
                omcen_service__service__service_name=form.instance.omcen_service.service.service_name,
                is_active=True
            ).first()
            before_service_in_use.is_active = False
            before_service_in_use.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_group'] = get_object_or_404(
            ServiceGroup,
            uuid=self.request.resolver_match.kwargs['pk']
        )
        context['before_service_in_use'] = ServiceInUse.objects.filter(
            omcen_user__username=self.request.user,
            omcen_service__service__service_name=context['service_group'].service.service_name,
            is_active=True
        ).exists()

        return context

    def get_success_url(self):
        service_group = get_object_or_404(
            ServiceGroup,
            uuid=self.request.resolver_match.kwargs['pk']
        )
        self.success_url = reverse_lazy(f'{service_group.service.service_name}:top')
        messages.success(self.request, _('登録が完了しました。'), extra_tags='success')

        return super().get_success_url()


# サービスの登録解除
class ServiceUnsubscribe(LoginRequiredMixin, UpdateView):
    template_name = 'omcen/service_unsubscribe.html'
    model = ServiceInUse
    form_class = ServiceUnsubscribeForm
    success_url = reverse_lazy('omcen:service_list')

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'))

            return self.handle_no_permission()

        if not ServiceInUse.objects.filter(uuid=self.request.resolver_match.kwargs['pk'], is_active=True).exists():
            return redirect(to=reverse('omcen:service_list'))

        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.is_active = False

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_in_use = get_object_or_404(
            ServiceInUse,
            uuid=self.request.resolver_match.kwargs['pk']
        )
        context['service_in_use'] = service_in_use
        context['cancel_url'] = f'{service_in_use.omcen_service.service.service_name}:top'

        return context

    def get_success_url(self):
        messages.success(self.request, _('登録が完了しました。'), extra_tags='success')

        return super().get_success_url()


# 使用中のサービス一覧
class ServiceInUseList(LoginRequiredMixin, ListView):
    template_name = 'omcen/service_in_use_list.html'
    model = ServiceInUse
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
            omcen_user__username=self.request.user,
            is_active=True
        )

        return query_set.order_by('omcen_service__service__service_name')


# omcenユーザーの停止
class OmcenUserDeactivate(LoginRequiredMixin, UpdateView):
    template_name = 'omcen/omcen_user_deactivate.html'
    model = OmcenUser
    form_class = OmcenUserDeactivateForm
    success_url = reverse_lazy('account_signup')

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'))

            return self.handle_no_permission()

        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.is_active = False
        ServiceInUse.objects.values().filter(
            omcen_user__username=self.request.user,
            is_active=True
        ).update(is_active=False)

        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _('アカウントの停止が完了しました'), extra_tags='success')

        return super().get_success_url()
