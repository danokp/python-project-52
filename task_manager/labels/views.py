from django.shortcuts import render, redirect
from django.views import View

from task_manager.mixins import UserLoginRequiredMixin
from .models import Label


class LabelView(UserLoginRequiredMixin, View):
    '''Show list of statuses.'''

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        return render(
            request,
            'labels/show_labels.html',
            context={'labels': labels}
        )


class LabelCreateView(UserLoginRequiredMixin, View):
    '''Create new status.'''
    pass


class LabelUpdateView(UserLoginRequiredMixin, View):
    '''Update status.'''
    pass


class LabelDeleteView(UserLoginRequiredMixin, View):
    '''Delete status.'''
    pass
