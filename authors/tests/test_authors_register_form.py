from unittest import TestCase
from .test_authors_base import AuthorsTestBase
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


class AuthorsRegisterFormIntegrationTest(AuthorsTestBase):

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
        # Creating a dummy user
        user = self.make_user()
        '''
        Updating the self.form to a local form data and putting the
        User object as an attribute
        '''
        data = self.form_data

        # Create a valid form
        form = RegisterForm(data=data)
        if form.is_valid():
            author = form.save(commit=False)
            author.user = user
            author.save()
        else:
            self.fail(msg="'form' must be valid")

        # Creating a invalid form data
        invalid_name = {'first_name': '123', 'last_name': '123'}
        invalid_passes = {'password': 'str@ngpass123',
                          'password_confirmation': 'wea&kpass123'}

        # Now, we update the form data
        data.update(invalid_name)
        data.update(invalid_passes)

        '''Creating a invalid form, invalid 'cause they can't recieve
        the same user, username & email'''
        form2 = RegisterForm(data=data)
        if form2.is_valid():
            self.fail("'form2' must be invalid")
        else:
            self.assertIn(field, form2.errors)
            self.assertEqual(form2.errors[field][0],
                             error_msg)

    @parameterized.expand([
        ('username', 'user'),
        ('first_name', 'first'),
        ('last_name', 'last'),
        ('email', 'email@anyemail.com'),
        ('password', 'Str0ngP@ssword1'),
        ('password_confirmation', 'Str0ngP@ssword1'),
    ])
    def test_check_validators_return_data(self, field, expected_value):
        form = RegisterForm(self.form_data)
        if form.is_valid():
            self.assertEqual(form.cleaned_data[field], expected_value)
        else:
            self.fail(msg="Form is not valid")

    def test_author_created_can_login(self):
        url = reverse('authors:treat')

        self.form_data.update({
            'username': 'testuser',
            'password': '@Bc123456',
            'password_confirmation': '@Bc123456',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='@Bc123456'
        )

        self.assertTrue(is_authenticated)