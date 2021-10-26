from pathlib import Path

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView

from config.public_key import Rsa
from config.settings import KEYS_DIR
from config.symmetric_key import Aes
from omcen.models import ServiceInUse
from password_box.forms import BoxCreateForm
from password_box.models import PasswordBox, PasswordBoxUser, PasswordBoxTag, PasswordBoxNonce


class Top(LoginRequiredMixin, ListView):
    template_name = 'password_box/top.html'
    model = PasswordBox
    paginate_by = 30
    ordering = 'is_active'
    form = None

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'), extra_tags='warning')

            return self.handle_no_permission()

        if not ServiceInUse.objects.filter(
                omcen_user__username=self.request.user,
                omcen_service__service__service_name__icontains='Password Box',
                is_active=True
        ).exists():
            messages.warning(self.request, _('パスワードボックスサービスを登録していません'), extra_tags='warning')
            return redirect(to=reverse('omcen:service_list'))

        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        query_set = super().get_queryset()
        query_set = query_set.filter(
            password_box_user__omcen_user__username=self.request.user,
            is_active=True
        )

        return query_set.order_by('box_name')


class BoxCreate(LoginRequiredMixin, CreateView):
    template_name = 'password_box/box_create.html'
    model = PasswordBox
    form_class = BoxCreateForm
    success_url = reverse_lazy('Password Box:top')

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'), extra_tags='warning')

            return self.handle_no_permission()

        if not ServiceInUse.objects.filter(
                omcen_user__username=self.request.user,
                omcen_service__service__service_name__icontains='Password Box',
                is_active=True
        ).exists():
            messages.warning(self.request, _('あなたはパスワードボックスサービスを登録していません'), extra_tags='warning')
            return redirect(to=reverse('omcen:service_list'))

        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.password_box_user = get_object_or_404(
            PasswordBoxUser,
            omcen_user=self.request.user
        )
        form.instance.box_name = form.cleaned_data['box_name']

        cipher_aes_generate_key = get_object_or_404(
            PasswordBoxUser,
            omcen_user=self.request.user
        ).aes_generation_key
        rsa = Rsa(
            secret_code_path=Path(KEYS_DIR, 'secret_code.bin'),
            rsa_key_path=Path(KEYS_DIR, 'rsa_key.pem')
        )
        private_key = rsa._private_key()
        aes = Aes(
            key=rsa.decryption(cipher_aes_generate_key, private_key)
        )

        self.cipher_user_name = aes.encryption(form.cleaned_data['user_name'].encode('utf-8'))
        self.cipher_password = aes.encryption(form.cleaned_data['password'].encode('utf-8'))
        self.cipher_email = aes.encryption(form.cleaned_data['email'].encode('utf-8'))

        form.instance.user_name = self.cipher_user_name[0]
        form.instance.password = self.cipher_password[0]
        form.instance.email = self.cipher_email[0]

        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.warning(self.request, _('すでに同じボックス名が存在します'), extra_tags='warning')

            return super().form_invalid(form)

    def create_done(self):
        try:
            PasswordBoxTag.objects.create(
                password_box=self.object,
                user_name_tag=self.cipher_user_name[1],
                password_tag=self.cipher_password[1],
                email_tag=self.cipher_email[1]
            )
            PasswordBoxNonce.objects.create(
                password_box=self.object,
                user_name_nonce=self.cipher_user_name[2],
                password_nonce=self.cipher_password[2],
                email_nonce=self.cipher_email[2]
            )
            messages.success(self.request, _('パスワードボックスの作成に成功しました'), extra_tags='success')
        except:
            self.object.delete()
            messages.error(self.request, _('パスワードボックスの作成に失敗しました'), extra_tags='error')

    def get_success_url(self):
        self.create_done()

        return super().get_success_url()
