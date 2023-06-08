from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    class Meta():
        model = User
        fields = ['first_name', 'last_name', 'username']
