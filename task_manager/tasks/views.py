from django.utils.translation import gettext as _
from django.contrib import messages
from django_filters.views import FilterView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Task
from .filters import TaskFilter
from task_manager.mixins import UserLoginRequiredMixin
from .forms import TaskCreationForm
from .mixins import TaskDeletionAccessMixin


class TaskListView(UserLoginRequiredMixin, FilterView):
    '''Show list of tasks'''

    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/task_list.html'
    extra_context = {'button_text': _('Show')}


class TaskView(UserLoginRequiredMixin, DetailView):
    '''Show task.'''

    model = Task


class TaskCreateView(UserLoginRequiredMixin, CreateView):
    '''Create new task.'''

    model = Task
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


class TaskUpdateView(UserLoginRequiredMixin, UpdateView):
    '''Update task.'''

    model = Task
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
    DeleteView,
):
    '''Delete task.'''

    model = Task
    success_url = reverse_lazy('show_tasks')
    template_name = 'tasks/delete_task.html'
    extra_context = {'button_text': _('Delete')}

    def post(self, request, *args, **kwargs):
        messages.success(self.request, _('Task has been deleted'))
        return super().post(request)
