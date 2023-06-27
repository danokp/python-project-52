from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import gettext as _

from task_manager.mixins import UserLoginRequiredMixin
from .models import Label
from .forms import LabelCreationForm


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
    pass


class LabelDeleteView(UserLoginRequiredMixin, View):
    '''Delete label.'''
    pass
