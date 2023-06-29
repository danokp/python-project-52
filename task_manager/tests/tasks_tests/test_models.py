from django.test import TestCase

from task_manager.tasks.models import Task


class TestTaskModels(TestCase):
    '''Test Label Model'''
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_model_fields(self):
        task_id = 1
        self.assertEquals(Task.objects.get(
            id=task_id).name,
            'Донести кольцо самостоятельно',
        )
        self.assertEquals(Task.objects.get(
            id=task_id).description,
            '''Путешествие стало слишком опасным для Братства кольца. Теперь мне предстоит нести Кольцо одному.''',  # noqa: E501
        )
        self.assertEquals(Task.objects.get(id=task_id).status.id, 1)
        self.assertEquals(Task.objects.get(id=task_id).creator.id, 1)
        self.assertEquals(Task.objects.get(id=task_id).executor.id, 1)
        for label, label_id in zip(
                Task.objects.get(id=task_id).labels.all(),
                (1, 2),
        ):
            self.assertEquals(label.id, label_id)
