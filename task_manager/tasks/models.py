from django.db import models

from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.labels.models import Label


class Task(models.Model):
    '''Task model'''
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(
        Status,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_tasks',
    )
    executor = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='executed_tasks',
    )
    label = models.ManyToManyField(
        Label,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
