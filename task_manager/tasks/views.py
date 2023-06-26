from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import gettext as _

from .models import Task
from .filters import TaskFilter

from .forms import TaskCreationForm


class TaskListView(View):
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


class TaskView(View):
    '''Show task.'''

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        return render(
            request,
            'tasks/task.html',
            context={'task': task}
        )


class TaskCreateView(View):
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
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            return redirect('show_tasks')
        return render(
            request,
            'tasks/create_task.html',
            context={'form': form, 'button_text': button_text},
        )


class TaskUpdateView(View):
    '''Update task.'''

    pass


class TaskDeleteView(View):
    '''Delete task.'''

    pass
