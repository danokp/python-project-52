from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import activate


class StatusLoggedInViewTest(TestCase):
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
            (self.statuses_url, 'statuses/show_statuses.html'),
            (self.create_status_url, 'statuses/create_status.html'),
            (self.update_status_url, 'statuses/update_status.html'),
            (self.delete_status_url, 'statuses/delete_status.html'),
            (self.delete_status_url_invalid_id, 'statuses/delete_status.html'),
        ]


    def test_status_get(self):
        for url, template in self.TESTDATA:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEquals(response.status_code, 200)
                self.assertTemplateUsed(response, template)


class StatusLoggedOutViewTest(StatusLoggedInViewTest):

    def setUp(self):
        super().setUp()

    def check_redirect(self, url):
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def check_redirect_page(self, url):
        '''Check page rendered after redirecting.'''
        response = self.client.get(url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_statuses_for_logged_out_users_get(self):
        self.client.logout()
        for url in self.TESTDATA:
            with self.subTest(url=url[0]):
                self.check_redirect(url[0])
                self.check_redirect_page(url[0])
