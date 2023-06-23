from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext as _


class HomePageView(TemplateView):
    '''Homepage.'''

    template_name = 'index.html'


class UserLoginView(View):
    '''Authorise the user.'''

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homepage')

        form = AuthenticationForm()
        button_text = _('Login')
        return render(
            request,
            'login.html',
            {'form': form, 'button_text': button_text},
        )

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user is not None:
            messages.success(request, _('You are logged in'))
            login(request, user)
            return redirect('homepage')
        messages.error(request, _('Enter the correct username and password, please. Both fields may be case-sensitive.'))
        form = AuthenticationForm(request.POST)
        # for f in form:
        #     print(f.name)
        button_text = _('Login')
        return render(
            request,
            'login.html',
            {'form': form, 'button_text': button_text},
        )


class UserLogoutView(View):
    '''Logout user.'''

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, _('You are logged out'))
        return redirect('homepage')


def error_404(request, exception):
    return render(request, '404.html')
