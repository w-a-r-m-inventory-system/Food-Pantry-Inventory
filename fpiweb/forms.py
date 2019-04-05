
from django.forms import CharField, Form, PasswordInput, ValidationError


class LoginForm(Form):

    username = CharField(
        label='Username',
        max_length=100,
    )

    password = CharField(
        label='Password',
        max_length=100,
        widget=PasswordInput
    )

# EOF