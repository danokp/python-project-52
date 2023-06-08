from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    '''User model.'''

    def __str__(self):
        return self.username
