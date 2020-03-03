

from django.contrib.auth.models import User


default_password = 'abc123'


def create_user(first_name, last_name):
    first_name = first_name.lower()
    last_name = last_name.lower()

    return User.objects.create_user(
        first_name[0] + last_name,
        f"{first_name}.{last_name}",
        default_password,
    )
