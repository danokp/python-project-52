from django.utils.translation import gettext as _
from django.contrib import messages
from django_filters.views import FilterView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from .models import Task
from .filters import TaskFilter
from task_manager.mixins import UserLoginRequiredMixin
from .forms import TaskCreationForm
from .mixins import TaskDeletionAccessMixin


class TaskBaseView:
    model = Task


class TaskListView(UserLoginRequiredMixin, TaskBaseView, FilterView):
    '''Show list of tasks'''

    filterset_class = TaskFilter
    template_name = 'tasks/task_list.html'
    extra_context = {'button_text': _('Show')}


class TaskView(UserLoginRequiredMixin, TaskBaseView, DetailView):
    '''Show task.'''


class TaskCreateView(UserLoginRequiredMixin, TaskBaseView, CreateView):
    '''Create new task.'''

    form_class = TaskCreationForm
    success_url = reverse_lazy('show_tasks')
    template_name = 'tasks/create_task.html'
    extra_context = {'button_text': _('Create')}

    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(
            self.request,
            _('Task has been created successfully'),
        )
        return super().form_valid(form)


class TaskUpdateView(UserLoginRequiredMixin, TaskBaseView, UpdateView):
    '''Update task.'''

    form_class = TaskCreationForm
    success_url = reverse_lazy('show_tasks')
    template_name = 'tasks/update_task.html'
    extra_context = {'button_text': _('Update')}

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Task has been updated successfully'),
        )
        return super().form_valid(form)


class TaskDeleteView(
    TaskDeletionAccessMixin,
    UserLoginRequiredMixin,
    TaskBaseView,
    DeleteView,
):
    '''Delete task.'''

    success_url = reverse_lazy('show_tasks')
    template_name = 'tasks/delete_task.html'
    extra_context = {'button_text': _('Delete')}

    def post(self, request, *args, **kwargs):
        messages.success(self.request, _('Task has been deleted'))
        return super().post(request)
