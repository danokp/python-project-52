import django_filters
from django import forms
from django.utils.translation import gettext as _

from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.models import User


class TaskFilter(django_filters.FilterSet):
    '''Filter for tasks filtering.'''
    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'),
    )

    self_tasks = django_filters.BooleanFilter(
        method='filter_created_by_logged_in_user',
        label=_('Created by me'),
        widget=forms.CheckboxInput(),
        required=False
    )

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Status'),
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_('Executor'),
    )

    def filter_created_by_logged_in_user(self, queryset, name, value):
        '''Filter tasks created by logged-in user.'''
        if value:
            # Filter tasks created by the logged-in user
            return queryset.filter(creator=self.request.user)
        else:
            return queryset

    class Meta:
        model = Task
        fields = [
            'status',
            'executor',
            'label',
            'self_tasks',
        ]
