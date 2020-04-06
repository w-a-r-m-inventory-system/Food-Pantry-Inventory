

from django.contrib.auth.models import User
from django.test import Client

from fpiweb.models import Profile

default_password = 'abc123'


def create_user(first_name, last_name):
    first_name = first_name.lower()
    last_name = last_name.lower()
    try:
        user = User.objects.get(
            first_name__iexact=first_name,
            last_name__iexact=last_name,
        )
    except User.DoesNotExist:
        user = User.objects.create_user(
            first_name[0] + last_name,
            f"{first_name}.{last_name}",
            default_password,
        )

    Profile.objects.get_or_create(
        user=user,
        defaults={
            'title': 'User',
        }
    )
    return user


def logged_in_user(first_name, last_name):
    user = create_user(first_name, last_name)
    client = Client()
    client.force_login(user)
    return client
