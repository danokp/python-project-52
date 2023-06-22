from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import gettext as _
from django.contrib import messages

from .models import Status
from .forms import StatusCreationForm


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
            messages.success(request, _('Статус успешно создан'))
            form.save()
            return redirect('show_statuses')
        return render(
            request,
            'statuses/create_status.html',
            context={'form': form, 'button_text': button_text},
        )





class StatusUpdateView(View):
    '''Update status.'''

    pass


class StatusDeleteView(View):
    '''Delete status.'''

    pass
