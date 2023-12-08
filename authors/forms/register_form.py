from django import forms
from django.core.exceptions import ValidationError
from authors.models import Authors
from utils.django_forms import add_placeholder


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Authors
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ------------ Placeholders ------------

        add_placeholder(self.fields['username'], 'Ex.: Mr. Cabaço')
        add_placeholder(self.fields['email'], 'youremail@mail.com')
        add_placeholder(self.fields['first_name'], 'Ex.: Davi')
        add_placeholder(self.fields['last_name'], 'Ex.: Souza')
        add_placeholder(self.fields['password'], 'Your password')
        add_placeholder(
            self.fields['password_confirmation'], 'Repeat your password')

    # ------- Putting the inputPassword widget & required validators -------

    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password field must not be empty'
        },)

    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Please, repeat your password'
        },)

    # ------- Putting required validators -------

    first_name = forms.CharField(
        error_messages={'required': 'First Name must not be empty'},
    )
    last_name = forms.CharField(
        error_messages={'required': 'Last Name must not be empty'},
    )
    username = forms.CharField(
        error_messages={'required': "Username field must not be empty"},
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail is required'},
    )

    # ------------ Validating the fields ------------

    def clean_username(self):
        username = self.cleaned_data['username']
        if Authors.objects.filter(username=username).exists():
            raise ValidationError('Username already exists!')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if Authors.objects.filter(email=email).exists():
            raise ValidationError('This e-mail is already in use!')
        return email

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        alphabet = list('abcdefghijklnmopqrstuvwxyz')

        for letter in data:
            if letter.lower() not in alphabet:
                raise ValidationError(
                    f"Don't write {letter} or anyone special character in this field",  # noqa
                    code='invalid',
                )

            return data

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')
        alphabet = list('abcdefghijklnmopqrstuvwxyz')

        for letter in data:
            if letter.lower() not in alphabet:
                raise ValidationError(
                    f"Don't write {letter} or anyone special character in this field",  # noqa
                    code='invalid',
                )

            return data

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            password_confirmation_error = ValidationError(
                'Password and password confirmation must be equal',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password_confirmation': [
                    password_confirmation_error,
                ],
            })
