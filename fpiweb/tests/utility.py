

from django.contrib.auth.models import Permission, User
from django.test import Client
from django.views import View

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
            # Added this line 6/22/20 per conversation with Travis
            # Required to run Selenium tests
            is_superuser=True,
        )

    Profile.objects.get_or_create(
        user=user,
        defaults={
            'title': 'User',
        }
    )
    return user


def logged_in_user(first_name: str, last_name: str, view=None) -> Client:
    user = create_user(first_name, last_name)
    if view is not None:
        grant_required_permissions(user, view)
    client = Client()
    client.force_login(user)
    return client


def grant_required_permissions(user:User, view:View) -> None:
    permissions = getattr(view, 'permission_required', [])
    for permission in permissions:
        pieces = permission.split('.')
        if len(pieces) != 2:
            raise RuntimeError(f"Cannot split {permission} into 2 pieces")
        app_label, codename = pieces

        print(f"codename={codename}")
        print(
            Permission.objects.filter(
                content_type__app_label=app_label,
                content_type__model='pallet',
            ).values_list(
                'content_type__app_label',
                'codename',
            )
        )

        try:
            permission = Permission.objects.get(
                content_type__app_label__iexact=app_label,
                codename__iexact=codename,
            )
        except Permission.DoesNotExist:
            raise RuntimeError(
                "Permission app_label={} codename={} not found".format(
                    app_label,
                    codename,
                )
            )
        user.user_permissions.add(permission)