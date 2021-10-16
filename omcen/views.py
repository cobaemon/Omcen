from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib import messages

from omcen.models import Service, Plan, ServiceGroup, ServiceInUse
from omcen.forms import SearchService, CreateServiceForm


# サービス管理画面
class ServiceControl(ListView):
    template_name = 'omcen/service_control.html'
    model = ServiceGroup
    paginate_by = 30
    ordering = 'is_active'
    form = None

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
class CreateService(CreateView):
    template_name = 'omcen/create_service.html'
    model = ServiceGroup
    form_class = CreateServiceForm
    success_url = reverse_lazy('omcen:service_control')
    
    def form_valid(self, form):
        # サービスを追加する場合、最低でも1つプランをセットする
        service = Service.objects.create(service_name=form.cleaned_data['service_name'])
        plan = Plan.objects.create(service_name=service,
                                   plan_name=form.cleaned_data['plan_name'],
                                   price=form.cleaned_data['price'])

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
