from django.test import TestCase
from django.contrib.auth.models import User


class AuthorsTestBase(TestCase):
    def setUp(self):

        # Form without User
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password_confirmation': 'Str0ngP@ssword1',
        }
        return super().setUp()

    def make_user(self):
        user = User.objects.create_user(
            username=self.form_data['username'],
            first_name=self.form_data['first_name'],
            last_name=self.form_data['last_name'],
            email=self.form_data['email'],
            password=self.form_data['password'],
        )
        return user
