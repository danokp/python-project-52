from django.db import models

# Create your models here.
class Label(models.Model):
    '''Label model'''
    name = models.CharField(max_length=250, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name