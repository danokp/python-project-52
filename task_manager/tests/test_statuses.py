from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import activate

from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusCreationForm


class TestStatusViewLoggedIn(TestCase):
    '''Test Status views for logged in users.'''
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        activate('en')
        self.client = Client()
        self.user = self.client.login(
            username='ring.bearer',
            password='frodo_124578',
        )

        self.statuses_url = reverse('show_statuses')
        self.create_status_url = reverse('create_status')
        self.update_status_url = reverse('update_status', kwargs={'pk': 1})
        self.delete_status_url = reverse('delete_status', kwargs={'pk': 1})
        self.delete_status_url_invalid_id = reverse(
            'delete_status',
            kwargs={'pk': 10},
        )

        self.TESTDATA = [
            (self.statuses_url, 'statuses/show_statuses.html', 200),
            (self.create_status_url, 'statuses/create_status.html', 200),
            (self.update_status_url, 'statuses/update_status.html', 200),
            (self.delete_status_url, 'statuses/delete_status.html', 200),
            (self.delete_status_url_invalid_id, '404.html', 404),
        ]


    def test_status_get(self):
        '''Test GET requests of CRUD'''
        for url, template, status_code in self.TESTDATA:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEquals(response.status_code, status_code)
                self.assertTemplateUsed(response, template)


    def test_status_create_post_valid_form(self):
        '''Test POST request to create new status'''
        status_name = 'in progress'
        response = self.client.post(
            self.create_status_url,
            data={'name': status_name},
        )
        self.assertEquals(response.status_code, 302)
        status = Status.objects.get(id=3)
        self.assertEquals(status.name, status_name)


    def test_status_create_post_invalid_form(self):
        '''Try to create Status with a name of an existing status.'''
        status_name = 'tested'
        response = self.client.post(
            self.create_status_url,
            data={'name': status_name},
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Status.objects.count(), 2)
        self.assertTemplateUsed(response, 'statuses/create_status.html')


    def test_status_update_post_valid_form(self):
        '''Test POST request to update status'''
        status_name = 'in progress'
        response = self.client.post(
            self.update_status_url,
            data={'name': status_name},
        )
        self.assertEquals(response.status_code, 302)
        status = Status.objects.get(id=1)
        self.assertEquals(status.name, status_name)


    def test_status_update_post_invalid_form(self):
        '''Try to update Status with a name of an existing status.'''
        status_name = 'new'
        response = self.client.post(
            self.update_status_url,
            data={'name': status_name},
        )
        self.assertEquals(response.status_code, 200)
        status = Status.objects.get(id=1)
        self.assertNotEqual(status.name, status_name)
        self.assertTemplateUsed(response, 'statuses/update_status.html')


    def test_status_delete_post(self):
        '''Test POST request to delete status'''
        response = self.client.post(self.delete_status_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Status.objects.count(), 1)


class TestStatusViewLoggedOut(TestStatusViewLoggedIn):
    '''Test Status views for logged-out users.'''
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

    def test_statuses_for_logged_out_users_get(self):
        '''Test statuses' CRUD is unavailable for logged out users.'''
        self.client.logout()
        for url in self.TESTDATA:
            with self.subTest(url=url[0]):
                self.check_redirect(url[0])
                self.check_redirect_page(url[0])


class TestStatusModels(TestCase):
    '''Test Status Model'''
    fixtures = ['statuses.json']

    def test_model_fields(self):
        self.assertEquals(Status.objects.get(id=1).name, 'tested')
        self.assertEquals(Status.objects.get(id=2).name, 'new')


class TestStatusForms(TestCase):
    '''Test Status Form'''
    def test_status_form_valid_data(self):
        form = StatusCreationForm(data={'name': 'in progress'})

        self.assertTrue(form.is_valid())

    def test_status_form_no_data(self):
        form = StatusCreationForm(data={})

        self.assertFalse(form.is_valid())
        # Check the amount of unfilled fields.
        self.assertEquals(len(form.errors), 1)
