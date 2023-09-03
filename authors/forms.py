from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, "placeholder", placeholder_val)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Mr. Cabaço')
        add_placeholder(self.fields['email'], 'youremail@mail.com')
        add_placeholder(self.fields['first_name'], 'Ex.: Davi')
        add_placeholder(self.fields['last_name'], 'Ex.: Souza')
        add_attr(self.fields['username'], 'css', 'a-css-class')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )
    )
    password2 = forms.CharField(
        required=True,
        label="Password Confirmation",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        help_texts = {
            'email': "The email must be valid.",
        }

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
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password confirmation must be equal',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
