from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView

from omcen.models import ServiceInUse
from tango.forms import VocabularyNotebookCreateForm, VocabularyNotebookUpdateForm, TangoCreateForm, TangoUpdateForm, \
    TangoSearchForm
from tango.models import VocabularyNotebook, Tango


# トップページ
class TopView(LoginRequiredMixin, ListView):
    template_name = 'tango/top.html'
    model = VocabularyNotebook
    paginate_by = 30
    ordering = 'vocabulary_notebook_name'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'), extra_tags='warning')

            return self.handle_no_permission()

        if not ServiceInUse.objects.filter(
                omcen_user__username=self.request.user,
                omcen_service__service__service_name__icontains='Tango',
                is_active=True
        ).exists():
            messages.warning(self.request, _('Tangoサービスを登録していません'), extra_tags='warning')

            return redirect(to=reverse('omcen:plan_selection', kwargs={'service_name': 'Tango'}))

        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        query_set = super().get_queryset()
        query_set = query_set.filter(
            omcen_user__username=self.request.user,
            is_active=True
        )

        return query_set.order_by('-created_at')


# 単語帳CRUD
class VocabularyNotebookCreateView(LoginRequiredMixin, CreateView):
    template_name = 'tango/vocabulary_notebook_create.html'
    model = VocabularyNotebook
    form_class = VocabularyNotebookCreateForm
    success_url = reverse_lazy('tango:top')

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'), extra_tags='warning')

            return self.handle_no_permission()

        if not ServiceInUse.objects.filter(
                omcen_user__username=self.request.user,
                omcen_service__service__service_name__icontains='Tango',
                is_active=True
        ).exists():
            messages.warning(self.request, _('Tangoサービスを登録していません'), extra_tags='warning')

            return redirect(to=reverse('omcen:plan_selection', kwargs={'service_name': 'Tango'}))

        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.omcen_user = self.request.user
        form.instance.vocabulary_notebook_name = form.cleaned_data['vocabulary_notebook_name']

        return super().form_valid(form)

    def form_invalid(self, form):
        if 'vocabulary_notebook_name' in form.errors:
            for ms in form.errors['vocabulary_notebook_name']:
                messages.error(self.request, f'{_("単語帳名")}: {ms}', extra_tags='error')

        return super().form_invalid(form)


class VocabularyNotebookReadView(LoginRequiredMixin, ListView):
    template_name = 'tango/vocabulary_notebook_read.html'
    model = Tango
    paginate_by = 30
    ordering = 'created_at'

    def __init__(self):
        super().__init__()
        self.form = TangoSearchForm()

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'), extra_tags='warning')

            return self.handle_no_permission()

        if not ServiceInUse.objects.filter(
                omcen_user__username=self.request.user,
                omcen_service__service__service_name__icontains='Tango',
                is_active=True
        ).exists():
            messages.warning(self.request, _('Tangoサービスを登録していません'), extra_tags='warning')

            return redirect(to=reverse('omcen:plan_selection', kwargs={'service_name': 'Tango'}))

        if not VocabularyNotebook.objects.filter(
                omcen_user__username=self.request.user,
                uuid=self.request.resolver_match.kwargs['pk']
        ).exists():
            messages.warning(self.request, _('単語帳が存在しません'), extra_tags='warning')

            return redirect(to=reverse('tango:top'))

        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        query_set = super().get_queryset()
        self.form = TangoSearchForm(self.request.GET or None)

        query_set = query_set.filter(
            vocabulary_notebook=get_object_or_404(VocabularyNotebook, omcen_user__username=self.request.user,
                                                  uuid=self.request.resolver_match.kwargs['pk'])
        )

        if self.form.is_bound:
            if self.form.is_valid():
                if self.form.cleaned_data['tango']:
                    tango = 'tango'
                    contents = 'contents'

                    tango_q = Q(**{tango: self.form.cleaned_data['tango']})
                    contents_q = Q()

                    if self.form.cleaned_data['search_type'] == '0':
                        tango += '__icontains'
                        tango_q = Q(**{tango: self.form.cleaned_data['tango']})

                        contents += '__icontains'

                    if self.form.cleaned_data['search_scope'] == '1':
                        contents_q = Q(**{contents: self.form.cleaned_data['tango']})

                    query_set = query_set.filter(
                        tango_q
                        |
                        contents_q
                    ).distinct()

                if not query_set.exists():
                    messages.info(self.request, _('該当する単語がありませんでした。'), extra_tags='info')

        return query_set.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = self.form
        context['vocabulary_notebook_uuid'] = self.request.resolver_match.kwargs['pk']
        context['vocabulary_notebook_name'] = get_object_or_404(
            VocabularyNotebook,
            omcen_user__username=self.request.user,
            uuid=self.request.resolver_match.kwargs['pk'],
        ).vocabulary_notebook_name

        if 'tango' in self.request.GET:
            context['tango'] = self.request.GET['tango']
            context['search_type'] = self.request.GET['search_type']
            context['search_scope'] = self.request.GET['search_scope']
        else:
            context['tango'] = ''
            context['search_type'] = 0
            context['search_scope'] = 0

        return context


class VocabularyNotebookUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'tango/vocabulary_notebook_update.html'
    model = VocabularyNotebook
    form_class = VocabularyNotebookUpdateForm
    success_url = reverse_lazy('tango:top')

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'), extra_tags='warning')

            return self.handle_no_permission()

        if not ServiceInUse.objects.filter(
                omcen_user__username=self.request.user,
                omcen_service__service__service_name__icontains='Tango',
                is_active=True
        ).exists():
            messages.warning(self.request, _('Tangoサービスを登録していません'), extra_tags='warning')

            return redirect(to=reverse('omcen:plan_selection', kwargs={'service_name': 'Tango'}))

        if not VocabularyNotebook.objects.filter(
                omcen_user__username=self.request.user,
                uuid=self.request.resolver_match.kwargs['pk']
        ).exists():
            messages.warning(self.request, _('単語帳が存在しません'), extra_tags='warning')

            return redirect(to=reverse('tango:top'))

        return super().dispatch(self.request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(VocabularyNotebookUpdateView, self).get_form_kwargs()

        kwargs['vocabulary_notebook_name'] = get_object_or_404(
            VocabularyNotebook,
            omcen_user__username=self.request.user,
            uuid=self.request.resolver_match.kwargs['pk'],
        ).vocabulary_notebook_name

        return kwargs

    def form_valid(self, form):
        form.instance.vocabulary_notebook_name = form.cleaned_data['vocabulary_notebook_name']

        return super().form_valid(form)

    def form_invalid(self, form):
        if 'vocabulary_notebook_name' in form.errors:
            for ms in form.errors['vocabulary_notebook_name']:
                messages.error(self.request, f'{_("単語帳名")}: {ms}', extra_tags='error')

        return super().form_invalid(form)


class VocabularyNotebookDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'tango/vocabulary_notebook_delete.html'
    model = VocabularyNotebook
    success_url = reverse_lazy('tango:top')

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'), extra_tags='warning')

            return self.handle_no_permission()

        if not ServiceInUse.objects.filter(
                omcen_user__username=self.request.user,
                omcen_service__service__service_name__icontains='Tango',
                is_active=True
        ).exists():
            messages.warning(self.request, _('Tangoサービスを登録していません'), extra_tags='warning')

            return redirect(to=reverse('omcen:plan_selection', kwargs={'service_name': 'Tango'}))

        if not VocabularyNotebook.objects.filter(
                omcen_user__username=self.request.user,
                uuid=self.request.resolver_match.kwargs['pk']
        ).exists():
            messages.warning(self.request, _('単語帳が存在しません'), extra_tags='warning')

            return redirect(to=reverse('tango:top'))

        return super().dispatch(self.request, *args, **kwargs)


# 単語CRUD
class TangoCreateView(LoginRequiredMixin, CreateView):
    template_name = 'tango/tango_create.html'
    model = Tango
    form_class = TangoCreateForm

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'), extra_tags='warning')

            return self.handle_no_permission()

        if not ServiceInUse.objects.filter(
                omcen_user__username=self.request.user,
                omcen_service__service__service_name__icontains='Tango',
                is_active=True
        ).exists():
            messages.warning(self.request, _('Tangoサービスを登録していません'), extra_tags='warning')

            return redirect(to=reverse('omcen:plan_selection', kwargs={'service_name': 'Tango'}))

        if not VocabularyNotebook.objects.filter(
                omcen_user__username=self.request.user,
                uuid=self.request.resolver_match.kwargs['vocabulary_notebook_pk']
        ).exists():
            messages.warning(self.request, _('単語帳が存在しません'), extra_tags='warning')

            return redirect(to=reverse('tango:top'))

        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['vocabulary_notebook_uuid'] = self.request.resolver_match.kwargs['vocabulary_notebook_pk']

        return context

    def form_valid(self, form):
        form.instance.vocabulary_notebook = get_object_or_404(
            VocabularyNotebook,
            omcen_user__username=self.request.user,
            uuid=self.request.resolver_match.kwargs['vocabulary_notebook_pk']
        )
        form.instance.tango = form.cleaned_data['tango']
        form.instance.contents = form.cleaned_data['contents']

        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, _('すでに同じ単語が存在します'), extra_tags='error')

            return super().form_invalid(form)

    def form_invalid(self, form):
        if 'tango' in form.errors:
            for ms in form.errors['tango']:
                messages.error(self.request, f'{_("単語")}: {ms}', extra_tags='error')

        if 'contents' in form.errors:
            for ms in form.errors['contents']:
                messages.error(self.request, f'{_("内容")}: {ms}', extra_tags='error')

        return super().form_invalid(form)

    def get_success_url(self):
        self.success_url = reverse_lazy('tango:vocabulary_notebook_read',
                                        kwargs={'pk': self.request.resolver_match.kwargs['vocabulary_notebook_pk']})

        return super().get_success_url()


class TangoReadView(LoginRequiredMixin, TemplateView):
    template_name = 'tango/tango_read.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'), extra_tags='warning')

            return self.handle_no_permission()

        if not ServiceInUse.objects.filter(
                omcen_user__username=self.request.user,
                omcen_service__service__service_name__icontains='Tango',
                is_active=True
        ).exists():
            messages.warning(self.request, _('Tangoサービスを登録していません'), extra_tags='warning')

            return redirect(to=reverse('omcen:plan_selection', kwargs={'service_name': 'Tango'}))

        if not VocabularyNotebook.objects.filter(
                omcen_user__username=self.request.user,
                uuid=self.request.resolver_match.kwargs['vocabulary_notebook_pk']
        ).exists():
            messages.warning(self.request, _('単語帳が存在しません'), extra_tags='warning')

            return redirect(to=reverse('tango:top'))

        if not Tango.objects.filter(uuid=self.request.resolver_match.kwargs['pk']).exists():
            messages.warning(self.request, _('単語が存在しません'), extra_tags='warning')

            return redirect(to=reverse('tango:vocabulary_notebook_read', kwargs={
                'vocabulary_notebook_pk': self.request.resolver_match.kwargs['vocabulary_notebook_pk']}))

        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['vocabulary_notebook_uuid'] = self.request.resolver_match.kwargs['vocabulary_notebook_pk']
        context['tango'] = get_object_or_404(
            Tango,
            uuid=self.request.resolver_match.kwargs['pk'],
        )

        return context


class TangoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'tango/tango_update.html'
    model = Tango
    form_class = TangoUpdateForm

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'), extra_tags='warning')

            return self.handle_no_permission()

        if not ServiceInUse.objects.filter(
                omcen_user__username=self.request.user,
                omcen_service__service__service_name__icontains='Tango',
                is_active=True
        ).exists():
            messages.warning(self.request, _('Tangoサービスを登録していません'), extra_tags='warning')

            return redirect(to=reverse('omcen:plan_selection', kwargs={'service_name': 'Tango'}))

        if not VocabularyNotebook.objects.filter(
                omcen_user__username=self.request.user,
                uuid=self.request.resolver_match.kwargs['vocabulary_notebook_pk']
        ).exists():
            messages.warning(self.request, _('単語帳が存在しません'), extra_tags='warning')

            return redirect(to=reverse('tango:top'))

        if not Tango.objects.filter(uuid=self.request.resolver_match.kwargs['pk']).exists():
            messages.warning(self.request, _('単語が存在しません'), extra_tags='warning')

            return redirect(to=reverse('tango:vocabulary_notebook_read',
                                       kwargs={'pk': self.request.resolver_match.kwargs['vocabulary_notebook_pk']}))

        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['vocabulary_notebook_uuid'] = self.request.resolver_match.kwargs['vocabulary_notebook_pk']

        return context

    def get_form_kwargs(self):
        kwargs = super(TangoUpdateView, self).get_form_kwargs()

        tango = get_object_or_404(
            Tango,
            uuid=self.request.resolver_match.kwargs['pk'],
        )
        kwargs['tango'] = tango.tango
        kwargs['contents'] = tango.contents

        return kwargs

    def form_valid(self, form):
        form.instance.tango = form.cleaned_data['tango']
        form.instance.contents = form.cleaned_data['contents']

        return super().form_valid(form)

    def form_invalid(self, form):
        if 'tango' in form.errors:
            for ms in form.errors['tango']:
                messages.error(self.request, f'{_("単語")}: {ms}', extra_tags='error')

        if 'contents' in form.errors:
            for ms in form.errors['contents']:
                messages.error(self.request, f'{_("内容")}: {ms}', extra_tags='error')

        return super().form_invalid(form)

    def get_success_url(self):
        self.success_url = reverse_lazy('tango:vocabulary_notebook_read',
                                        kwargs={'pk': self.request.resolver_match.kwargs['vocabulary_notebook_pk']})

        return super().get_success_url()


class TangoDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'tango/tango_delete.html'
    model = Tango

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _('ログインしてください'), extra_tags='warning')

            return self.handle_no_permission()

        if not ServiceInUse.objects.filter(
                omcen_user__username=self.request.user,
                omcen_service__service__service_name__icontains='Tango',
                is_active=True
        ).exists():
            messages.warning(self.request, _('Tangoサービスを登録していません'), extra_tags='warning')

            return redirect(to=reverse('omcen:plan_selection', kwargs={'service_name': 'Tango'}))

        if not VocabularyNotebook.objects.filter(
                omcen_user__username=self.request.user,
                uuid=self.request.resolver_match.kwargs['vocabulary_notebook_pk']
        ).exists():
            messages.warning(self.request, _('単語帳が存在しません'), extra_tags='warning')

            return redirect(to=reverse('tango:top'))

        if not Tango.objects.filter(uuid=self.request.resolver_match.kwargs['pk']).exists():
            messages.warning(self.request, _('単語が存在しません'), extra_tags='warning')

            return redirect(to=reverse('tango:vocabulary_notebook_read',
                                       kwargs={'pk': self.request.resolver_match.kwargs['vocabulary_notebook_pk']}))

        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['vocabulary_notebook_uuid'] = self.request.resolver_match.kwargs['vocabulary_notebook_pk']

        return context

    def get_success_url(self):
        self.success_url = reverse_lazy('tango:vocabulary_notebook_read',
                                        kwargs={'pk': self.request.resolver_match.kwargs['vocabulary_notebook_pk']})

        return super().get_success_url()
