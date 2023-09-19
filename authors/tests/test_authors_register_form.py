from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized
from authors.forms import RegisterForm, Authors
from authors.models import User


class AuthorsRegisterFormUnittest(TestCase):

    @parameterized.expand([
        ('username', 'Ex.: Mr. Cabaço'),
        ('email', 'youremail@mail.com'),
        ('first_name', 'Ex.: Davi'),
        ('last_name', 'Ex.: Souza'),
        ('password', 'Your password'),
        ('password_confirmation', 'Repeat your password'),
    ])
    def test_placeholder_fields(self, field, expected_placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, expected_placeholder)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password_confirmation', 'Password Confirmation'),
    ])
    def test_fields_label(self, field, needed):
        current = Authors._meta.get_field(field).verbose_name
        self.assertEqual(current, needed)


class AuthorsRegisterFormIntegrationTest(DjangoTestCase):

    def setUp(self, *args, **kwargs):
        # Making a dummy form data:
        form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password_confirmation': 'Str0ngP@ssword1',
        }

        # Making a dummy user:
        dummy_user = User.objects.create_user(
            username=form_data['username'],
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            email=form_data['email'],
            password=form_data['password'],
        )
        # Adding the User object to our future Author object as an attribute
        form_data.update({'user': dummy_user})

        # Some tests needs just a form data, not a instance of Authors class:
        self.form_data = form_data

        # Instanciating an Authors object:
        self.form = Authors.objects.create(
            user=dummy_user,
            username=form_data['username'],
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            email=form_data['email'],
            password=form_data['password'],
            password_confirmation=form_data['password_confirmation']
        )

        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Username field must not be empty'),
        ('first_name', 'First Name must not be empty'),
        ('last_name', 'Last Name must not be empty'),
        ('password', 'Password field must not be empty'),
        ('password_confirmation', 'Please, repeat your password'),
        ('email', 'E-mail is required'),
    ])
    def test_fields_required_validation(self, field, msg):
        # Updating the field value to a blank field,
        self.form_data[field] = ''
        url = reverse('authors:treat')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    @parameterized.expand([
        ('username', 'Username already exists!'),
        ('email', 'This e-mail is already in use!'),
        ('first_name', "Don't write 1 or anyone special character in this field"),  # noqa
        ('last_name', "Don't write 1 or anyone special character in this field"),  # noqa
        ('password', 'Password and password confirmation must be equal'),
        ('password_confirmation', 'Password and password confirmation must be equal'),   # noqa
    ])
    def test_clean_fields_validation(self, field, error_msg):
        invalid_name = {'first_name': '123', 'last_name': '123'}
        invalid_passes = {'password': 'str@ngpass123',
                          'password_confirmation': 'wea&kpass123'}
        # Updating the form data with invalid names
        data = self.form_data
        data.update(invalid_name)
        data.update(invalid_passes)

        '''Creating a invalid form, invalid 'cause they can't recieve
        the same user, username & email'''
        self.form2 = RegisterForm(data=self.form_data)
        self.assertFalse(self.form2.is_valid())
        self.assertIn(field, self.form2.errors)
        self.assertEqual(self.form2.errors[field][0],
                         error_msg)
