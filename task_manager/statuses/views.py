from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from task_manager.mixins import UserLoginRequiredMixin
from .models import Status
from .forms import StatusCreationForm
from task_manager.tasks.models import Task


class StatusView(UserLoginRequiredMixin, ListView):
    '''Show list of statuses.'''

    model = Status


class StatusCreateView(UserLoginRequiredMixin, CreateView):
    '''Create new status.'''

    model = Status
    form_class = StatusCreationForm
    success_url = reverse_lazy('show_statuses')
    template_name = 'statuses/create_status.html'
    extra_context = {'button_text': _('Create')}

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Status has been created successfully'),
        )
        return super().form_valid(form)


class StatusUpdateView(UserLoginRequiredMixin, UpdateView):
    '''Update status.'''

    model = Status
    form_class = StatusCreationForm
    success_url = reverse_lazy('show_statuses')
    template_name = 'statuses/update_status.html'
    extra_context = {'button_text': _('Update')}

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Status has been updated successfully'),
        )
        return super().form_valid(form)


class StatusDeleteView(UserLoginRequiredMixin, DeleteView):
    '''Delete status.'''

    model = Status
    success_url = reverse_lazy('show_statuses')
    template_name = 'statuses/delete_status.html'
    extra_context = {'button_text': _('Delete')}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        related_tasks = Task.objects.filter(status=self.object)
        if related_tasks.exists():
            messages.error(
                request,
                _('Cannot delete status. There are related tasks.'),
            )
            return redirect('show_statuses')
        messages.success(self.request, _('Status has been deleted'))
        return super().post(request)
