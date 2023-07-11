from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.list import ListView

from .forms import UserRegistrationForm
from .models import User
from .mixins import UserAccessMixin
from task_manager.tasks.models import Task


class UsersView(ListView):
    '''Show list of users.'''

    model = User


class UserCreateView(CreateView):
    '''Create new user.'''

    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'users/create_user.html'
    extra_context = {'button_text': pgettext_lazy('Button name', 'Sign Up')}

    def form_valid(self, form):
        messages.success(
            self.request,
            _('The user has been registered successfully'),
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class UserUpdateView(UserAccessMixin, UpdateView):
    '''Update user profile.'''

    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('show_users')
    template_name = 'users/update_user.html'
    extra_context = {'button_text': _('Update')}

    def form_valid(self, form):
        messages.success(
            self.request,
            _('The user has been updated successfully'),
        )
        return super().form_valid(form)


class UserDeleteView(UserAccessMixin, DeleteView):
    '''Delete user.'''

    model = User
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
