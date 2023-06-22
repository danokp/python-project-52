from django.db import models

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __srt__(self):
        return self.name
