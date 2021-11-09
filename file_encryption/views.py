from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from file_encryption.forms import TopForm
from file_encryption.models import FileEncryptionUser
from omcen.models import ServiceInUse


# トップ画面
class Top(LoginRequiredMixin, FormView):
    template_name = 'file_encryption/top.html'
    model = FileEncryptionUser
    form_class = TopForm

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'), extra_tags='warning')

            return self.handle_no_permission()

        if not ServiceInUse.objects.filter(
                omcen_user__username=self.request.user,
                omcen_service__service__service_name__icontains='File Encryption',
                is_active=True
        ).exists():
            messages.warning(self.request, _('ファイル暗号化サービスを登録していません'), extra_tags='warning')

            return redirect(to=reverse('omcen:plan_selection', kwargs={'service_name': 'File Encryption'}))

        return super().dispatch(self.request, *args, **kwargs)
