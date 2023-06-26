from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    '''User model.'''

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
