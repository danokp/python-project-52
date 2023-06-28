from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import activate

from task_manager.tasks.models import Task


class TestTaskViewLoggedIn(TestCase):
    '''Test Label views for logged in users.'''
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        activate('en')
        self.client = Client()
        self.user = self.client.login(
            username='ring.bearer',
            password='frodo_124578',
        )

        self.tasks_url = reverse('show_tasks')
        self.create_task_url = reverse('create_task')
        self.task_url = reverse('task', kwargs={'pk': 1})
        self.task_url_invalid_id = reverse('task', kwargs={'pk': 10})
        self.update_task_url = reverse('update_task', kwargs={'pk': 1})
        self.delete_task_url = reverse('delete_task', kwargs={'pk': 1})
        self.delete_task_url_invalid_id = reverse(
            'delete_label',
            kwargs={'pk': 10},
        )

        self.TESTDATA = [
            (self.tasks_url, 'tasks/show_tasks.html', 200),
            (self.task_url, 'tasks/task.html', 200),
            (self.task_url_invalid_id, '404.html', 404),
            (self.create_task_url, 'tasks/create_task.html', 200),
            (self.update_task_url, 'tasks/update_task.html', 200),
            (self.delete_task_url, 'tasks/delete_task.html', 200),
            (self.delete_task_url_invalid_id, '404.html', 404),
        ]

    def test_tasks_get(self):
        '''Test GET requests of CRUD'''
        for url, template, status_code in self.TESTDATA:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEquals(response.status_code, status_code)
                self.assertTemplateUsed(response, template)

    def test_task_create_post_valid_form(self):
        '''Test POST request to create new task'''
        task_count_before_changes = Task.objects.count()
        task_name = 'Скрыться от орков'
        task_description = 'Близко к Роковой горе Кольцо лучше не использовать'
        task_status = 2
        task_executor = 1
        task_label = [2]
        response = self.client.post(
            self.create_task_url,
            data={
                'name': task_name,
                'description': task_description,
                'status': task_status,
                'executor': task_executor,
                'label': task_label,
            },
        )
        self.assertEquals(response.status_code, 302)
        task = Task.objects.get(id=task_count_before_changes + 1)
        self.assertEquals(Task.objects.count(), task_count_before_changes + 1)
        self.assertEquals(task.name, task_name)
        self.assertEquals(task.description, task_description)
        self.assertEquals(task.status.id, task_status)
        self.assertEquals(task.executor.id, task_executor)
        self.assertEquals(task.creator.id, task_executor)
        self.assertEquals(task.label.all()[0].id, task_label[0])

    def test_task_create_post_invalid_form(self):
        '''Try to create Task with a name of an existing task.'''
        task_count_before_changes = Task.objects.count()
        response = self.client.post(
            self.create_task_url,
            data={},
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Task.objects.count(), task_count_before_changes)
        self.assertTemplateUsed(response, 'tasks/create_task.html')

    def test_task_update_post_valid_form(self):
        '''Test POST request to update task'''
        task_count_before_changes = Task.objects.count()
        task_name = 'Скрыться от орков'
        task_description = 'Близко к Роковой горе Кольцо лучше не использовать'
        task_status = 2
        task_executor = 1
        task_label = [3]
        response = self.client.post(
            self.update_task_url,
            data={
                'name': task_name,
                'description': task_description,
                'status': task_status,
                'executor': task_executor,
                'label': task_label,
            },
        )
        self.assertEquals(response.status_code, 302)
        task = Task.objects.get(id=1)
        self.assertEquals(Task.objects.count(), task_count_before_changes)
        self.assertEquals(task.name, task_name)
        self.assertEquals(task.description, task_description)
        self.assertEquals(task.status.id, task_status)
        self.assertEquals(task.executor.id, task_executor)
        self.assertEquals(task.creator.id, task_executor)
        self.assertEquals(task.label.all()[0].id, task_label[0])

    def test_task_delete_post(self):
        '''Test POST request to delete task'''
        task_count_before_changes = Task.objects.count()
        response = self.client.post(self.delete_task_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Task.objects.count(), task_count_before_changes - 1)


class TestTaskViewLoggedOut(TestTaskViewLoggedIn):
    '''Test Task views for logged-out users.'''
    def setUp(self):
        super().setUp()

    def check_redirect(self, url):
        '''Check if redirect is successful.'''
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def check_redirect_page(self, url):
        '''Check page rendered after redirecting.'''
        response = self.client.get(url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_tasks_for_logged_out_users_get(self):
        '''Test tasks' CRUD is unavailable for logged out users.'''
        self.client.logout()
        for url in self.TESTDATA:
            with self.subTest(url=url[0]):
                self.check_redirect(url[0])
                self.check_redirect_page(url[0])
