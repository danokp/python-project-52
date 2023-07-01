from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.translation import pgettext
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import UserRegistrationForm
from .models import User
from .mixins import UserAccessMixin
from task_manager.tasks.models import Task
from task_manager.logging_config import logger


class UsersView(View):
    '''Show list of users.'''

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(
            request,
            'users/show_users.html',
            context={'users': users}
        )


class UserFormCreateView(CreateView):
    '''Create new user.'''

    model = User
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


class UserUpdateView(UserAccessMixin, View):
    '''Update user profile.'''

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)
        form = UserRegistrationForm(instance=user)
        button_text = _('Update')
        return render(
            request,
            'users/update_user.html',
            {'form': form, 'button_text': button_text},
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            messages.success(
                request,
                _('The user has been updated successfully'),
            )
            form.save()
            return redirect('show_users')
        button_text = _('Update')
        return render(
            request,
            'users/update_user.html',
            {'form': form, 'button_text': button_text},
        )


class UserDeleteView(UserAccessMixin, View):
    '''Delete user.'''

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)
        return render(request, 'users/delete_user.html', {'user': user})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)
        related_tasks = Task.objects.filter(Q(creator=user) | Q(executor=user))
        if related_tasks.exists():
            messages.error(
                request,
                _('Cannot delete user. There are related tasks.'),
            )
            return redirect('show_users')
        messages.success(request, _('The user has been deleted'))
        user.delete()
        return redirect('show_users')
