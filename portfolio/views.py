import smtplib

from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from portfolio.forms import EmailForm


# メッセージ送信
def send_message(form):
    try:
        send_mail(
            form.cleaned_data['email_title'],
            form.cleaned_data['email_message'],
            # 'mgnco@outlook.jp',
            'pb.officialteam@gmail.com',
            ['mgnco@outlook.jp'],
            fail_silently=False
        )
    except smtplib.SMTPException:
        return False

    return True


# トップページ
class Top(FormView):
    template_name = 'portfolio/top.html'
    form_class = EmailForm
    success_url = reverse_lazy('Portfolio:top')

    def form_valid(self, form):
        if send_message(form):
            messages.success(self.request, _('メッセージの送信に成功しました'), extra_tags='success')

            return super().form_valid(form)
        else:
            messages.error(self.request, _('メッセージの送信に失敗しました'), extra_tags='error')

            return super().form_invalid(form)


# プロフィール
class Profile(FormView):
    template_name = 'portfolio/profile.html'
    form_class = EmailForm
    success_url = reverse_lazy('Portfolio:profile')

    def form_valid(self, form):
        if send_message(form):
            messages.success(self.request, _('メッセージの送信に成功しました'), extra_tags='success')

            return super().form_valid(form)
        else:
            messages.error(self.request, _('メッセージの送信に失敗しました'), extra_tags='error')

            return super().form_invalid(form)


# 成果物一覧ページ
class Deliverables(FormView):
    template_name = 'portfolio/deliverables.html'
    form_class = EmailForm
    success_url = reverse_lazy('Portfolio:deliverables')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['deliverables'] = [
            ['単語帳', '単語帳をWeb上で再現しました', 'Portfolio:vocabulary_notebook'],
        ]

        return context

    def form_valid(self, form):
        if send_message(form):
            messages.success(self.request, _('メッセージの送信に成功しました'), extra_tags='success')

            return super().form_valid(form)
        else:
            messages.error(self.request, _('メッセージの送信に失敗しました'), extra_tags='error')

            return super().form_invalid(form)


# 成果物 単語帳
class VocabularyNotebook(FormView):
    template_name = 'portfolio/vocabulary_notebook.html'
    form_class = EmailForm
    success_url = reverse_lazy('Portfolio:vocabulary_notebook')

    def form_valid(self, form):
        if send_message(form):
            messages.success(self.request, _('メッセージの送信に成功しました'), extra_tags='success')

            return super().form_valid(form)
        else:
            messages.error(self.request, _('メッセージの送信に失敗しました'), extra_tags='error')

            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deliverables_url'] = reverse_lazy('Tango:top')
        context['login_url'] = '/accounts/login'
        context['signup_url'] = '/accounts/signup'
        context['service_list_url'] = reverse_lazy('Omcen:service_list')

        return context