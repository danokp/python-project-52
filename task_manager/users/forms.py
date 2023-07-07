from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]
