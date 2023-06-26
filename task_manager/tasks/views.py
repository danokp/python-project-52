from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext as _

from .models import Task
from .filters import TaskFilter

from task_manager.statuses.models import Status
from task_manager.users.models import User


class TaskListView(View):
    '''Show list of tasks'''

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        tasks = Task.objects.all()
        users = User.objects.all()
        filtered_tasks = TaskFilter(
            request.GET,
            queryset=tasks,
            request=request,
        )
        button_text = _('Show')
        return render(
            request,
            'tasks/show_tasks.html',
            context={'tasks': tasks, 'statuses': statuses, 'users': users, 'filtered_tasks': filtered_tasks, 'button_text': button_text},
        )


class TaskView(View):
    '''Show task.'''

    pass


class TaskCreateView(View):
    '''Create new task.'''

    pass


class TaskUpdateView(View):
    '''Update task.'''

    pass


class TaskDeleteView(View):
    '''Delete task.'''

    pass
