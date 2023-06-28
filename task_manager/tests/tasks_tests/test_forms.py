from django.test import TestCase

from task_manager.users.models import User
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.forms import TaskCreationForm


class TestTaskForms(TestCase):
    '''Test Task Form'''
    fixtures = ['users.json', 'statuses.json', 'labels.json']

    def test_task_form_valid_data(self):
        form = TaskCreationForm(
            data={
                'name': 'Донести кольцо самостоятельно',
                'description': 'Путешествие стало слишком опасным',
                'status': Status.objects.get(id=1),
                'creator': User.objects.get(id=1),
                'executor': User.objects.get(id=1),
                'label': [Label.objects.get(id=1), Label.objects.get(id=2)],
            }
        )
        self.assertTrue(form.is_valid())

    def test_task_form_no_data(self):
        form = TaskCreationForm(data={})
        self.assertFalse(form.is_valid())
        # Check the amount of unfilled fields.
        self.assertEquals(len(form.errors), 1)
