from django.shortcuts import render
from django.views import View

from task_manager.statuses.models import Status


class StatusView(View):
    '''Show list of statuses.'''

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(
            request,
            'statuses/show_statuses.html',
            context={'statuses': statuses},
        )


class StatusCreateView(View):
    '''Create new status.'''

    pass


class StatusUpdateView(View):
    '''Update status.'''

    pass


class StatusDeleteView(View):
    '''Delete status.'''

    pass
