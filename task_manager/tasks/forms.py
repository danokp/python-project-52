from django import forms
from django.utils.translation import gettext as _

from .models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.labels.models import Label


class TaskCreationForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'))
    description = forms.CharField(
        label=_('Description'),
        required=False,
        widget=forms.Textarea(attrs={"rows": "5"}),
    )
    status = forms.ModelChoiceField(
        label=_('Status'),
        queryset=Status.objects.all(),
        required=False,
    )
    executor = forms.ModelChoiceField(
        label=_('Executor'),
        queryset=User.objects.all(),
        required=False,
    )
    label = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
    )

    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'executor',
            'label',
        ]
