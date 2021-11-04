from pathlib import Path

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, TemplateView, DeleteView, UpdateView, FormView

from config.exception import DataCorruptedError
from config.public_key import Rsa
from config.settings import KEYS_DIR
from config.symmetric_key import Aes
from omcen.models import ServiceInUse
from password_box.forms import BoxCreateForm, BoxDeleteForm, BoxUpdateForm, PasswordGenerateForm
from password_box.models import PasswordBox, PasswordBoxUser, PasswordBoxTag, PasswordBoxNonce


# トップ画面
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

            return redirect(to=reverse('omcen:plan_selection', kwargs={'service_name': 'Password Box'}))

        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        query_set = super().get_queryset()
        query_set = query_set.filter(
            password_box_user__omcen_user__username=self.request.user,
            is_active=True
        )

        return query_set.order_by('box_name')


# パスワード生成
class PasswordGenerate(LoginRequiredMixin, FormView):
    template_name = 'password_box/password_generate.html'
    form_class = PasswordGenerateForm

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

            return redirect(to=reverse('omcen:plan_selection', kwargs={'service_name': 'Password Box'}))

        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        self.success_url = reverse_lazy('Password Box:create',
                                        kwargs={'password_type': self.request.POST['password_type'],
                                                'password_num': self.request.POST['password_num']})

        return super().get_success_url()


# 新規作成
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

    def get_form_kwargs(self):
        kwargs = super(BoxCreate, self).get_form_kwargs()
        if 'password_type' in self.request.resolver_match.kwargs:
            kwargs['password_type'] = self.request.resolver_match.kwargs['password_type']
            kwargs['password_num'] = self.request.resolver_match.kwargs['password_num']

        return kwargs

    def form_valid(self, form):
        form.instance.password_box_user = get_object_or_404(
            PasswordBoxUser,
            omcen_user=self.request.user,
            is_active=True
        )
        form.instance.box_name = form.cleaned_data['box_name']

        cipher_aes_generate_key = get_object_or_404(
            PasswordBoxUser,
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
            messages.success(self.request, _('ボックスの作成に成功しました'), extra_tags='success')
        except:
            self.object.delete()
            messages.error(self.request, _('ボックスの作成に失敗しました'), extra_tags='error')

    def get_success_url(self):
        self.create_done()

        return super().get_success_url()


# 表示
class BoxView(LoginRequiredMixin, TemplateView):
    template_name = 'password_box/box_view.html'

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

        password_box = get_object_or_404(
            PasswordBox,
            uuid=self.request.resolver_match.kwargs['pk'],
        )
        if password_box.password_box_user.omcen_user.username != str(self.request.user):
            messages.warning(self.request, _('不正な値を受け取りました'), extra_tags='warning')

            return redirect(to=reverse('Password Box:top'))

        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        password_box = get_object_or_404(
            PasswordBox,
            uuid=self.request.resolver_match.kwargs['pk'],
        )

        cipher_aes_generate_key = get_object_or_404(
            PasswordBoxUser,
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

        password_box_tag = get_object_or_404(
            PasswordBoxTag,
            password_box=password_box
        )
        password_box_nonce = get_object_or_404(
            PasswordBoxNonce,
            password_box=password_box
        )

        user_name = aes.decryption(
            cipher_data=password_box.user_name,
            tag=password_box_tag.user_name_tag,
            nonce=password_box_nonce.user_name_nonce
        )
        password = aes.decryption(
            cipher_data=password_box.password,
            tag=password_box_tag.password_tag,
            nonce=password_box_nonce.password_nonce
        )
        email = aes.decryption(
            cipher_data=password_box.email,
            tag=password_box_tag.email_tag,
            nonce=password_box_nonce.email_nonce
        )

        if user_name[1] != ValueError or password[1] != ValueError or email[1] != ValueError:
            messages.success(self.request, _('読み込みに成功しました'), extra_tags='success')
        if user_name[1] == ValueError:
            messages.error(self.request, _('ユーザー名の読み込みに失敗しました'), extra_tags='error')
        if password[1] == ValueError:
            messages.error(self.request, _('パスワードの読み込みに失敗しました'), extra_tags='error')
        if email[1] == ValueError:
            messages.error(self.request, _('メールアドレスの読み込みに失敗しました'), extra_tags='error')

        if user_name[1] == DataCorruptedError:
            messages.warning(self.request, _('ユーザー名が改ざんされている恐れがあります'), extra_tags='warning')
        if password[1] == DataCorruptedError:
            messages.warning(self.request, _('パスワードが改ざんされている恐れがあります'), extra_tags='warning')
        if email[1] == DataCorruptedError:
            messages.warning(self.request, _('メールアドレスが改ざんされている恐れがあります'), extra_tags='warning')

        context['box_name'] = password_box.box_name
        context['box_uuid'] = password_box.uuid
        context['box_user_name'] = user_name[0].decode('utf-8')
        context['box_password'] = password[0].decode('utf-8')
        context['box_email'] = email[0].decode('utf-8')

        return context


# 削除
class BoxDelete(LoginRequiredMixin, DeleteView):
    template_name = 'password_box/box_delete.html'
    model = PasswordBox
    form_class = BoxDeleteForm

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

        password_box = get_object_or_404(
            PasswordBox,
            uuid=self.request.resolver_match.kwargs['pk'],
        )
        if password_box.password_box_user.omcen_user.username != str(self.request.user):
            messages.warning(self.request, _('不正な値を受け取りました'), extra_tags='warning')

            return redirect(to=reverse('Password Box:top'))

        return super().dispatch(self.request, *args, **kwargs)

    def success_done(self):
        get_object_or_404(
            PasswordBoxTag,
            password_box=self.object
        ).delete()
        get_object_or_404(
            PasswordBoxNonce,
            password_box=self.object
        ).delete()

    def get_success_url(self):
        self.success_url = reverse_lazy('Password Box:top')
        self.success_done()
        messages.success(self.request, _('削除に成功しました'), extra_tags='success')

        return super().get_success_url()


# 編集
class BoxUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'password_box/box_update.html'
    model = PasswordBox
    form_class = BoxUpdateForm

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

        password_box = get_object_or_404(
            PasswordBox,
            uuid=self.request.resolver_match.kwargs['pk'],
        )
        if password_box.password_box_user.omcen_user.username != str(self.request.user):
            messages.warning(self.request, _('不正な値を受け取りました'), extra_tags='warning')

            return redirect(to=reverse('Password Box:top'))

        return super().dispatch(self.request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(BoxUpdate, self).get_form_kwargs()

        password_box = get_object_or_404(
            PasswordBox,
            uuid=self.request.resolver_match.kwargs['pk'],
        )
        cipher_aes_generate_key = get_object_or_404(
            PasswordBoxUser,
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

        password_box_tag = get_object_or_404(
            PasswordBoxTag,
            password_box=password_box
        )
        password_box_nonce = get_object_or_404(
            PasswordBoxNonce,
            password_box=password_box
        )

        user_name = aes.decryption(
            cipher_data=password_box.user_name,
            tag=password_box_tag.user_name_tag,
            nonce=password_box_nonce.user_name_nonce
        )
        password = aes.decryption(
            cipher_data=password_box.password,
            tag=password_box_tag.password_tag,
            nonce=password_box_nonce.password_nonce
        )
        email = aes.decryption(
            cipher_data=password_box.email,
            tag=password_box_tag.email_tag,
            nonce=password_box_nonce.email_nonce
        )

        if user_name[1] != ValueError or password[1] != ValueError or email[1] != ValueError:
            messages.success(self.request, _('読み込みに成功しました'), extra_tags='success')
        if user_name[1] == ValueError:
            messages.error(self.request, _('ユーザー名の読み込みに失敗しました'), extra_tags='error')
        if password[1] == ValueError:
            messages.error(self.request, _('パスワードの読み込みに失敗しました'), extra_tags='error')
        if email[1] == ValueError:
            messages.error(self.request, _('メールアドレスの読み込みに失敗しました'), extra_tags='error')

        if user_name[1] == DataCorruptedError:
            messages.warning(self.request, _('ユーザー名が改ざんされている恐れがあります'), extra_tags='warning')
        if password[1] == DataCorruptedError:
            messages.warning(self.request, _('パスワードが改ざんされている恐れがあります'), extra_tags='warning')
        if email[1] == DataCorruptedError:
            messages.warning(self.request, _('メールアドレスが改ざんされている恐れがあります'), extra_tags='warning')

        kwargs['box_name'] = password_box.box_name
        kwargs['user_name'] = user_name[0].decode('utf-8')
        kwargs['password'] = password[0].decode('utf-8')
        kwargs['email'] = email[0].decode('utf-8')

        return kwargs

    def form_valid(self, form):
        form.instance.password_box_user = get_object_or_404(
            PasswordBoxUser,
            omcen_user=self.request.user,
            is_active=True
        )
        form.instance.box_name = form.cleaned_data['box_name']

        cipher_aes_generate_key = get_object_or_404(
            PasswordBoxUser,
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

        self.cipher_user_name = aes.encryption(form.cleaned_data['user_name'].encode('utf-8'))
        self.cipher_password = aes.encryption(form.cleaned_data['password'].encode('utf-8'))
        self.cipher_email = aes.encryption(form.cleaned_data['email'].encode('utf-8'))

        form.instance.box_name = form.cleaned_data['box_name']
        form.instance.user_name = self.cipher_user_name[0]
        form.instance.password = self.cipher_password[0]
        form.instance.email = self.cipher_email[0]

        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.warning(self.request, _('すでに同じボックス名が存在します'), extra_tags='warning')

            return super().form_invalid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     password_box = get_object_or_404(
    #         PasswordBox,
    #         uuid=self.request.resolver_match.kwargs['pk'],
    #     )
    #
    #     cipher_aes_generate_key = get_object_or_404(
    #         PasswordBoxUser,
    #         omcen_user=self.request.user,
    #         is_active=True
    #     ).aes_generation_key
    #     rsa = Rsa(
    #         secret_code_path=Path(KEYS_DIR, 'secret_code.bin'),
    #         rsa_key_path=Path(KEYS_DIR, 'rsa_key.pem')
    #     )
    #     private_key = rsa._private_key()
    #     aes = Aes(
    #         key=rsa.decryption(cipher_aes_generate_key, private_key)
    #     )
    #
    #     password_box_tag = get_object_or_404(
    #         PasswordBoxTag,
    #         password_box=password_box
    #     )
    #     password_box_nonce = get_object_or_404(
    #         PasswordBoxNonce,
    #         password_box=password_box
    #     )
    #
    #     user_name = aes.decryption(
    #         cipher_data=password_box.user_name,
    #         tag=password_box_tag.user_name_tag,
    #         nonce=password_box_nonce.user_name_nonce
    #     )
    #     password = aes.decryption(
    #         cipher_data=password_box.password,
    #         tag=password_box_tag.password_tag,
    #         nonce=password_box_nonce.password_nonce
    #     )
    #     email = aes.decryption(
    #         cipher_data=password_box.email,
    #         tag=password_box_tag.email_tag,
    #         nonce=password_box_nonce.email_nonce
    #     )
    #
    #     if user_name[1] != ValueError or password[1] != ValueError or email[1] != ValueError:
    #         messages.success(self.request, _('読み込みに成功しました'), extra_tags='success')
    #     if user_name[1] == ValueError:
    #         messages.error(self.request, _('ユーザー名の読み込みに失敗しました'), extra_tags='error')
    #     if password[1] == ValueError:
    #         messages.error(self.request, _('パスワードの読み込みに失敗しました'), extra_tags='error')
    #     if email[1] == ValueError:
    #         messages.error(self.request, _('メールアドレスの読み込みに失敗しました'), extra_tags='error')
    #
    #     if user_name[1] == DataCorruptedError:
    #         messages.warning(self.request, _('ユーザー名が改ざんされている恐れがあります'), extra_tags='warning')
    #     if password[1] == DataCorruptedError:
    #         messages.warning(self.request, _('パスワードが改ざんされている恐れがあります'), extra_tags='warning')
    #     if email[1] == DataCorruptedError:
    #         messages.warning(self.request, _('メールアドレスが改ざんされている恐れがあります'), extra_tags='warning')
    #
    #     context['form'] = BoxUpdateForm(initial={
    #         'box_name': password_box.box_name,
    #         'user_name': user_name[0].decode('utf-8'),
    #         'password': password[0].decode('utf-8'),
    #         'email': email[0].decode('utf-8')
    #     })
    #     context['box_name'] = password_box.box_name
    #
    #     return context

    def success_done(self):
        try:
            PasswordBoxTag.objects.values().filter(
                password_box=self.object
            ).update(
                user_name_tag=self.cipher_user_name[1],
                password_tag=self.cipher_password[1],
                email_tag=self.cipher_email[1]
            )
            PasswordBoxNonce.objects.values().filter(
                password_box=self.object
            ).update(
                user_name_nonce=self.cipher_user_name[2],
                password_nonce=self.cipher_password[2],
                email_nonce=self.cipher_email[2]
            )
            messages.success(self.request, _('編集に成功しました'), extra_tags='success')
        except:
            self.object.delete()
            messages.error(self.request, _('編集に失敗しました'), extra_tags='error')

    def get_success_url(self):
        self.success_url = reverse_lazy('Password Box:top')
        self.success_done()

        return super().get_success_url()
