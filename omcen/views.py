from django.views.generic import ListView
from django.contrib import messages

from omcen.models import Service, Plan, ServiceGroup, ServiceInUse
from omcen.forms import SearchService


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
