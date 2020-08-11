from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission, User
from django.test import Client
from django.views import View

from fpiweb.constants import AccessLevel, TargetUser
from fpiweb.models import Profile

default_password = 'abc123'


class ManageUserPermissions(object):
    pass



def create_user(*,
                username: str,
                first_name: str = 'first',
                last_name: str = 'last',
                title: str = 'title',
                password: str = default_password,
                access: AccessLevel = AccessLevel.Volunteer,
                ):
    user_model = get_user_model()
    username = username.lower()
    first_name = first_name.lower()
    last_name = last_name.lower()

    # Try to find an existing user with this username. If no match, create a
    # user, but with separate code so the real code can be properly tested.
    try:
        user = user_model.objects.get(
            username__exact=username,
        )
    except user_model.DoesNotExist:
        user = user_model.objects.create_user(
            username=username,
            first_name=first_name,
            last_name= last_name,
        )
        user.save()

    # add or update the user's profile
    try:
        profile = Profile.objects.get(
            user=user,
        )
        profile.title = title
        profile.save()
    except Profile.DoesNotExist:
        profile = Profile.objects.create(
            user = user,
            title = title,
        )

    # fix up group permissions
    grp_vol = Group.objects.get(name=AccessLevel.Volunteer._name_)
    grp_staff = Group.objects.get(name=AccessLevel.Staff._name_)
    grp_admin = Group.objects.get(name=AccessLevel.Admin._name_)
    user.groups.clear()
    user.groups.add(grp_vol)
    if access > AccessLevel.Volunteer:
        user.groups.add(grp_staff)
        if access > AccessLevel.Staff:
            user.groups.add(grp_admin)
    return user


def logged_in_user(first_name: str, last_name: str, view=None) -> Client:
    user = create_user(username='user')
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