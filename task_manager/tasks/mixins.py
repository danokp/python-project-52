from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from .models import Task


class TaskDeletionAccessMixin(UserPassesTestMixin):

    def test_func(self):
        task_id = self.kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        return self.request.user == task.creator

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("Task may be deleted only by its creator"),
        )
        return redirect('show_tasks')
