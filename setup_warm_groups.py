#!/usr/bin/env python

# Boilerplate for stand-alone Django scripts
from django import setup
setup()

# ---------------------------------------------------------

from sys import stderr

from django.contrib.auth.models import Group, Permission


GROUPS_AND_PERMISSIONS = {
    'Volunteers': (
        ('fpiweb', 'box', 'add_box'),
        ('fpiweb', 'box', 'check_in_box'),
        ('fpiweb', 'box', 'check_out_box'),
        ('fpiweb', 'box', 'move_box'),
        ('fpiweb', 'box', 'view_box'),
        ('fpiweb', 'pallet', 'build_pallet'),
        ('fpiweb', 'pallet', 'move_pallet'),
        ('fpiweb', 'pallet', 'view_pallet'),
    ),
    'Staff': (
        
    ),
}


def setup_group_permissions(group, permissions):

    print(f"Clearing {group.name} permissions.")
    group.permissions.clear()

    for app_label, model, codename in permissions:
        try:
            permission = Permission.objects.get(
                content_type__app_label=app_label,
                content_type__model=model,
                codename=codename
            )
        except Permission.DoesNotExist:
            print(f"Permission {model} {codename} not found", file=stderr)
            continue

        print(f"Granting {model} {codename} to {group.name}")
        group.permissions.add(permission)


def setup_groups_and_permissions(groups_and_permissions):
    for group_name, permissions in groups_and_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Created {group_name} group.")
        else:
            print(f"Found {group_name} group.")

        setup_group_permissions(group, permissions)
        print()


setup_groups_and_permissions(GROUPS_AND_PERMISSIONS)






