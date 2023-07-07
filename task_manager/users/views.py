from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.translation import pgettext
from django.db.models import Q
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from .forms import UserRegistrationForm
from .models import User
from .mixins import UserAccessMixin
from task_manager.tasks.models import Task
from task_manager.logging_config import logger


class UserBaseView:
    model = User


class UsersView(UserBaseView, ListView):
    '''Show list of users.'''


class UserFormCreateView(UserBaseView, CreateView):
    '''Create new user.'''

    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'users/create_user.html'
    extra_context = {'button_text': pgettext('Button name', 'Sign Up')}

    def form_valid(self, form):
        logger.debug('The user has been registered successfully')
        messages.success(
            self.request,
            _('The user has been registered successfully'),
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.error('The user has not been registered')
        return super().form_invalid(form)


class UserUpdateView(UserAccessMixin, UserBaseView, UpdateView):
    '''Update user profile.'''

    form_class = UserRegistrationForm
    success_url = reverse_lazy('show_users')
    template_name = 'users/update_user.html'
    extra_context = {'button_text': _('Update')}


class UserDeleteView(UserAccessMixin, UserBaseView, DeleteView):
    '''Delete user.'''

    success_url = reverse_lazy('show_users')
    template_name = 'users/delete_user.html'
    extra_context = {'button_text': _('Delete')}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        related_tasks = Task.objects.filter(
            Q(creator=self.object) | Q(executor=self.object)
        )
        if related_tasks.exists():
            messages.error(
                request,
                _('Cannot delete user. There are related tasks.'),
            )
            return redirect('show_users')
        messages.success(self.request, _('The user has been deleted'))
        return super().post(request)
