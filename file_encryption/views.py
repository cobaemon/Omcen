from pathlib import Path

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from config.public_key import Rsa
from config.settings import KEYS_DIR
from config.symmetric_key import Aes
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

    def form_valid(self, form):
        cipher_aes_generate_key = get_object_or_404(
            FileEncryptionUser,
            omcen_user=self.request.user,
            is_active=True
        ).aes_generation_key
        rsa = Rsa(
            secret_code_path=Path(KEYS_DIR, 'secret_code.bin'),
            rsa_key_path=Path(KEYS_DIR, 'rsa_key.pem')
        )
        private_key = rsa._private_key()
        aes = Aes(
            key=rsa.decryption(cipher_aes_generate_key, private_key)
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        self.success_url = reverse_lazy('File Encryption:top')

        return super().get_success_url()
