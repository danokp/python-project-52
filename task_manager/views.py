from django.views.generic.base import TemplateView
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.translation import pgettext
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .logging_config import logger


class HomePageView(TemplateView):
    '''Homepage.'''

    template_name = 'index.html'


class UserLoginView(LoginView):
    '''Authorise the user.'''
    template_name = 'login.html'
    extra_context = {'button_text': pgettext('Button name', 'Login')}
    success_url = reverse_lazy('homepage')

    def form_invalid(self, form):
        logger.error('Log in error')
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        logger.debug('Logged in successfully')
        messages.success(self.request, _('You are logged in'))
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    '''Logout user.'''

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
