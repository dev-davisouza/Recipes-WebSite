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

    @parameterized.expand([
        ('username', (
            'Obrigatório. 150 caracteres ou menos. '
            'Letras, números e @/./+/-/_ apenas.')),
        ('email', 'The e-mail must be valid.'),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)
