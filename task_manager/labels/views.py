from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import get_object_or_404

from task_manager.mixins import UserLoginRequiredMixin
from .models import Label
from .forms import LabelCreationForm
from task_manager.tasks.models import Task


class LabelView(UserLoginRequiredMixin, View):
    '''Show list of labels.'''

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        return render(
            request,
            'labels/show_labels.html',
            context={'labels': labels}
        )


class LabelCreateView(UserLoginRequiredMixin, View):
    '''Create new label.'''

    def get(self, request, *args, **kwargs):
        form = LabelCreationForm()
        button_text = _('Create')
        return render(
            request,
            'labels/create_label.html',
            context={'form': form, 'button_text': button_text},
        )

    def post(self, request, *args, **kwargs):
        form = LabelCreationForm(request.POST)

        if form.is_valid():
            messages.success(request, _('Label has been created successfully'))
            form.save()
            return redirect('show_labels')

        button_text = _('Create')
        return render(
            request,
            'labels/create_label.html',
            context={'form': form, 'button_text': button_text},
        )


class LabelUpdateView(UserLoginRequiredMixin, View):
    '''Update label.'''

    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        label = get_object_or_404(Label, id=label_id)
        form = LabelCreationForm(instance=label)
        button_text = _('Update')
        return render(
            request,
            'labels/update_label.html',
            context={'form': form, 'button_text': button_text},
        )

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        label = get_object_or_404(Label, id=label_id)
        form = LabelCreationForm(request.POST, instance=label)

        if form.is_valid():
            messages.success(request, _('Label has been updated successfully'))
            form.save()
            return redirect('show_labels')

        button_text = _('Update')
        return render(
            request,
            'labels/update_label.html',
            context={'form': form, 'button_text': button_text},
        )


class LabelDeleteView(UserLoginRequiredMixin, View):
    '''Delete label.'''
    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        label = get_object_or_404(Label, id=label_id)
        return render(
            request,
            'labels/delete_label.html',
            context={'label': label},
        )

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        label = get_object_or_404(Label, id=label_id)
        related_tasks = Task.objects.filter(labels=label)
        if related_tasks.exists():
            messages.error(
                request,
                _('Cannot delete label. There are related tasks.'),
            )
            return redirect('show_labels')

        messages.success(request, _('Label has been deleted'))
        label.delete()
        return redirect('show_labels')
