from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .mixin import UserLoginRequiredMixin
from .models import Status
from .forms import StatusCreationForm


class StatusView(UserLoginRequiredMixin, View):
    '''Show list of statuses.'''

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(
            request,
            'statuses/show_statuses.html',
            context={'statuses': statuses},
        )


class StatusCreateView(UserLoginRequiredMixin, View):
    '''Create new status.'''

    def get(self, request, *args, **kwargs):
        form = StatusCreationForm()
        button_text = _('Create')
        return render(
            request,
            'statuses/create_status.html',
            context={'form': form, 'button_text': button_text},
        )

    def post(self, request, *args, **kwargs):
        form = StatusCreationForm(request.POST)
        button_text = _('Create')

        if form.is_valid():
            messages.success(request, _('Status created successfully'))
            form.save()
            return redirect('show_statuses')
        return render(
            request,
            'statuses/create_status.html',
            context={'form': form, 'button_text': button_text},
        )


class StatusUpdateView(UserLoginRequiredMixin, View):
    '''Update status.'''

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        status = get_object_or_404(Status, id=status_id)
        form = StatusCreationForm(instance=status)
        button_text = _('Update')
        return render(
            request,
            'statuses/update_status.html',
            context={'form': form, 'button_text': button_text},
        )


    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        status = get_object_or_404(Status, id=status_id)
        form = StatusCreationForm(request.POST, instance=status)

        if form.is_valid():
            messages.success(request, _('Status updated successfully'))
            form.save()
            return redirect('show_statuses')
        button_text = _('Update')
        return render(
            request,
            'statuses/update_status.html',
            context={'form': form, 'button_text': button_text},
        )


class StatusDeleteView(UserLoginRequiredMixin, View):
    '''Delete status.'''

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        status = get_object_or_404(Status, id=status_id)
        return render(
            request,
            'statuses/delete_status.html',
            context={'status': status}
        )

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        status = get_object_or_404(Status, id=status_id)
        messages.success(request, _('Status deleted'))
        status.delete()
        return redirect('show_statuses')
