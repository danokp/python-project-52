from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class UserLoginRequiredMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                _('You are not logged in! Log in, please.'),
            )
            return redirect('login')
