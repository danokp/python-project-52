from django.contrib.auth.forms import UserCreationForm
# from django.utils.translation import gettext as _
# from django import forms

from .models import User


class UserRegistrationForm(UserCreationForm):
    # first_name = forms.CharField(label=_('First name'))
    # last_name = forms.CharField(label='Last name')
    class Meta():
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]
