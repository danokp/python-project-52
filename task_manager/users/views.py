from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import UserRegistrationForm
from .models import User
from .mixin import UserAccessMixin


class UsersView(View):
    '''Show list of users.'''

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(
            request,
            'users/show_users.html',
            context={'users': users}
        )

class UserFormCreateView(View):
    '''Create new user.'''

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homepage')

        form = UserRegistrationForm()
        button_text = _('Sign Up')
        return render(
            request,
            'users/create_user.html',
            {'form': form, 'button_text': button_text},
        )

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        button_text = _('Sign Up')
        if form.is_valid():
            messages.success(request, _('The user has been registered successfully'))
            form.save()
            return redirect('login')
        return render(
            request,
            'users/create_user.html',
            {'form': form, 'button_text': button_text},
        )

class UserUpdateView(UserAccessMixin, View):
    '''Update user profile.'''

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        form = UserRegistrationForm(instance=user)
        button_text = _('Update')
        return render(
            request,
            'users/update_user.html',
            {'form': form, 'button_text': button_text},
        )

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, _('The user has been updated successfully'))
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
        user = User.objects.get(id=user_id)
        return render(request, 'users/delete_user.html', {'user': user})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        if user:
            messages.success(request, _('The user has been deleted'))
            user.delete()
        return redirect('show_users')
