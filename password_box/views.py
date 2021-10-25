from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from omcen.models import ServiceInUse
from password_box.models import PasswordBox


class Top(LoginRequiredMixin, ListView):
    template_name = 'password_box/top.html'
    model = PasswordBox
    paginate_by = 30
    ordering = 'is_active'
    form = None

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'))

            return self.handle_no_permission()

        if not ServiceInUse.objects.filter(
                omcen_user__username=self.request.user,
                omcen_service__service__service_name__icontains='Password Box',
                is_active=True
        ).exists():
            messages.warning(self.request, _('パスワードボックスサービスを登録していません'))
            return redirect(to=reverse('omcen:service_list'))

        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        query_set = super().get_queryset()
        query_set = query_set.filter(
            password_box_user__omcen_user__username=self.request.user,
            is_active=True
        )

        return query_set.order_by('box_name')
