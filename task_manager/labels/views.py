from django.shortcuts import render, redirect
from django.views import View

from task_manager.mixins import UserLoginRequiredMixin



class LabelView(UserLoginRequiredMixin, View):
    '''Show list of statuses.'''
    pass


class LabelCreateView(UserLoginRequiredMixin, View):
    '''Create new status.'''
    pass


class LabelUpdateView(UserLoginRequiredMixin, View):
    '''Update status.'''
    pass


class LabelDeleteView(UserLoginRequiredMixin, View):
    '''Delete status.'''
    pass
