from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from task_manager.mixins import UserLoginRequiredMixin
from .models import Status
from .forms import StatusCreationForm
from task_manager.tasks.models import Task


class StatusBaseView:
    model = Status


class StatusView(UserLoginRequiredMixin, StatusBaseView, ListView):
    '''Show list of statuses.'''


class StatusCreateView(UserLoginRequiredMixin, StatusBaseView, CreateView):
    '''Create new status.'''

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


class StatusUpdateView(UserLoginRequiredMixin, StatusBaseView, UpdateView):
    '''Update status.'''

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


class StatusDeleteView(UserLoginRequiredMixin, StatusBaseView, DeleteView):
    '''Delete status.'''

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
