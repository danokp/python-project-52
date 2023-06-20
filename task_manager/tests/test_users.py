from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from django.utils.translation import activate

from task_manager.users.models import User
# from task_manager.users.views import UsersView
#
# import json


# class TestUrls(SimpleTestCase):
#     # fixtures = ['urls.json']
#
#     def test_show_users_url_resolves(self):
#         url_ = reverse('show_users')
#         print(resolve(url_))
#         self.assertEquals(resolve(url_).func.view_class, UsersView)

class UserViewTests(TestCase):

    def setUp(self):
        activate("en")
        self.client = Client()

        self.users_url = reverse('show_users')
        self.create_user_url = reverse('create_user')

    def test_user_show_users_get(self):
        response = self.client.get(self.users_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/show_users.html')


    def test_user_create_post_valid_form(self):
        response = self.client.post(self.create_user_url, data={
            'username': 'mr.grey',
            'first_name': 'Gandalf',
            'last_name': 'Grey',
            'password1': 'gandalf_124578',
            'password2': 'gandalf_124578',
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.count(), 1)


    def test_user_create_post_invalid_form(self):
        response = self.client.post(self.create_user_url, data={})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(User.objects.count(), 0)
        self.assertTemplateUsed(response, 'users/create_user.html')


class LoggedInUserViewTests(TestCase):
    fixtures = ['users.json']
    def setUp(self):
        activate("en")
        self.client = Client()
        self.update_user_url = reverse('update_user', kwargs={'pk': 1})
        self.delete_user_url = reverse('delete_user', kwargs={'pk': 1})
        self.delete_user_url_invalid_id = reverse(
            'delete_user',
            kwargs={'pk': 10},
        )

        # user_password = 'frodo_124578'
        # test_user = User.objects.create_user(
        #     username='frodo',
        #     first_name='Frodo',
        #     last_name='Baggins',
        #     password=user_password
        # )
        # test_user = User.objects.get(id=1)
        # self.client.login(
        #     username=test_user.username,
        #     password=test_user.password1,
        # )
        self.client.login(
            username='ring.bearer',
            password='frodo_124578',
        )
        # self.client.force_login(test_user)

    def test_user_update_get(self):
        response = self.client.get(self.update_user_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update_user.html')

    def test_user_update_post(self):
        response = self.client.post(self.update_user_url, data={
            'username': 'mr.grey',
            'first_name': 'Gandalf',
            'last_name': 'Grey',
            'password1': 'gandalf_124578',
            'password2': 'gandalf_124578',
        })
        self.assertEquals(response.status_code, 302)
        user = User.objects.get(id=1)
        self.assertEquals(user.username, 'mr.grey')

    def test_user_delete_get(self):
        response = self.client.get(self.delete_user_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete_user.html')

    def test_user_delete_post(self):
        response = self.client.post(self.delete_user_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.count(), 0)
