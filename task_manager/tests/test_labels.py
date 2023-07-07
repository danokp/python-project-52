from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import activate

from task_manager.labels.models import Label
from task_manager.labels.forms import LabelCreationForm


class TestLabelViewLoggedIn(TestCase):
    '''Test Label views for logged in users.'''
    fixtures = ['users.json', 'labels.json']

    def setUp(self):
        activate('en')
        self.client = Client()
        self.user = self.client.login(
            username='ring.bearer',
            password='frodo_124578',
        )

        self.labels_url = reverse('show_labels')
        self.create_label_url = reverse('create_label')
        self.update_label_url = reverse('update_label', kwargs={'pk': 1})
        self.delete_label_url = reverse('delete_label', kwargs={'pk': 1})
        self.delete_label_url_invalid_id = reverse(
            'delete_label',
            kwargs={'pk': 10},
        )

        self.TESTDATA = [
            (self.labels_url, 'labels/label_list.html', 200),
            (self.create_label_url, 'labels/create_label.html', 200),
            (self.update_label_url, 'labels/update_label.html', 200),
            (self.delete_label_url, 'labels/delete_label.html', 200),
            (self.delete_label_url_invalid_id, '404.html', 404),
        ]

    def test_labels_get(self):
        '''Test GET requests of CRUD'''
        for url, template, status_code in self.TESTDATA:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEquals(response.status_code, status_code)
                self.assertTemplateUsed(response, template)

    def test_label_create_post_valid_form(self):
        '''Test POST request to create new label'''
        label_count_before_changes = Label.objects.count()
        label_name = 'Fellowship of the Ring'
        response = self.client.post(
            self.create_label_url,
            data={'name': label_name},
        )
        self.assertEquals(response.status_code, 302)
        label = Label.objects.get(id=label_count_before_changes + 1)
        self.assertEquals(
            Label.objects.count(),
            label_count_before_changes + 1,
        )
        self.assertEquals(label.name, label_name)

    def test_label_create_post_invalid_form(self):
        '''Try to create Label with a name of an existing label.'''
        label_count_before_changes = Label.objects.count()
        label_name = 'Lord of the rings'
        response = self.client.post(
            self.create_label_url,
            data={'name': label_name},
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Label.objects.count(), label_count_before_changes)
        self.assertTemplateUsed(response, 'labels/create_label.html')

    def test_label_update_post_valid_form(self):
        '''Test POST request to update label'''
        label_name = 'tested'
        response = self.client.post(
            self.update_label_url,
            data={'name': label_name},
        )
        self.assertEquals(response.status_code, 302)
        label = Label.objects.get(id=1)
        self.assertEquals(label.name, label_name)

    def test_label_update_post_invalid_form(self):
        '''Try to update Label with a name of an existing label.'''
        label_name = 'Mount Doom'
        response = self.client.post(
            self.update_label_url,
            data={'name': label_name},
        )
        self.assertEquals(response.status_code, 200)
        label = Label.objects.get(id=1)
        self.assertNotEqual(label.name, label_name)
        self.assertTemplateUsed(response, 'labels/update_label.html')

    def test_label_delete_post(self):
        '''Test POST request to delete label'''
        label_count_before_changes = Label.objects.count()
        response = self.client.post(self.delete_label_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(
            Label.objects.count(),
            label_count_before_changes - 1,
        )


class TestLabelViewLoggedOut(TestLabelViewLoggedIn):
    '''Test Label views for logged-out users.'''
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

    def test_labels_for_logged_out_users_get(self):
        '''Test labels' CRUD is unavailable for logged out users.'''
        self.client.logout()
        for url in self.TESTDATA:
            with self.subTest(url=url[0]):
                self.check_redirect(url[0])
                self.check_redirect_page(url[0])


class TestLabelModels(TestCase):
    '''Test Label Model'''
    fixtures = ['labels.json']

    def test_model_fields(self):
        self.assertEquals(Label.objects.get(id=1).name, 'Lord of the rings')
        self.assertEquals(Label.objects.get(id=2).name, 'Mount Doom')
        self.assertEquals(Label.objects.get(id=3).name, 'Best friend')


class TestLabelForms(TestCase):
    '''Test Label Form'''
    def test_label_form_valid_data(self):
        form = LabelCreationForm(data={'name': 'Lord of the rings'})

        self.assertTrue(form.is_valid())

    def test_label_form_no_data(self):
        form = LabelCreationForm(data={})

        self.assertFalse(form.is_valid())
        # Check the amount of unfilled fields.
        self.assertEquals(len(form.errors), 1)
