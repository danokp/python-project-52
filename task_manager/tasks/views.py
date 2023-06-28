from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import Task
from .filters import TaskFilter
from task_manager.mixins import UserLoginRequiredMixin
from .forms import TaskCreationForm


class TaskListView(UserLoginRequiredMixin, View):
    '''Show list of tasks'''

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        filtered_tasks = TaskFilter(
            request.GET,
            queryset=tasks,
            request=request,
        )
        button_text = _('Show')
        return render(
            request,
            'tasks/show_tasks.html',
            context={
                'filtered_tasks': filtered_tasks,
                'button_text': button_text,
            },
        )


class TaskView(UserLoginRequiredMixin, View):
    '''Show task.'''

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, id=task_id)
        return render(
            request,
            'tasks/task.html',
            context={'task': task}
        )


class TaskCreateView(UserLoginRequiredMixin, View):
    '''Create new task.'''

    def get(self, request, *args, **kwargs):
        form = TaskCreationForm()
        button_text = _('Create')
        return render(
            request,
            'tasks/create_task.html',
            context={'form': form, 'button_text': button_text},
        )

    def post(self, request, *args, **kwargs):
        form = TaskCreationForm(request.POST)
        button_text = _('Create')

        if form.is_valid():
            messages.success(request, _('Task created successfully'))
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            form.save_m2m()
            return redirect('show_tasks')
        return render(
            request,
            'tasks/create_task.html',
            context={'form': form, 'button_text': button_text},
        )


class TaskUpdateView(UserLoginRequiredMixin, View):
    '''Update task.'''

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, id=task_id)
        form = TaskCreationForm(instance=task)
        button_text = _('Update')
        return render(
            request,
            'tasks/update_task.html',
            context={'form': form, 'button_text': button_text},
        )

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, id=task_id)
        form = TaskCreationForm(request.POST, instance=task)
        if form.is_valid():
            messages.success(request, _('Task updated successfully'))
            form.save()
            return redirect('show_tasks')

        button_text = _('Update')
        return render(
            request,
            'tasks/update_task.html',
            context={'form': form, 'button_text': button_text},
        )


class TaskDeleteView(UserLoginRequiredMixin, View):
    '''Delete task.'''

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, id=task_id)
        return render(
            request,
            'tasks/delete_task.html',
            context={'task': task}
        )

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, id=task_id)
        messages.success(request, _('Task deleted'))
        task.delete()
        return redirect('show_tasks')
