from django.test import TestCase
from parameterized import parameterized
from authors.forms import RegisterForm


class AuthorsUnittest(TestCase):

    @parameterized.expand([
        ('username', 'Mr. Cabaço'),
        ('email', 'youremail@mail.com'),
        ('first_name', 'Ex.: Davi'),
        ('last_name', 'Ex.: Souza'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_placeholder_fields(self, field, expected_placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, expected_placeholder)
