#!/usr/bin/env python

# Boilerplate for stand-alone Django scripts
from django import setup
setup()

# ---------------------------------------------------------

from sys import stderr

from django.contrib.auth.models import Group, Permission


GROUPS_AND_PERMISSIONS = {
    'Volunteers': {
        'fpiweb': {
            'box': [
                'add_box',
                'check_in_box',
                'check_out_box',
                'move_box',
                'view_box'
            ],
            'pallet': [
                'build_pallet',
                'move_pallet',
                'view_pallet',
            ],
        },
    },
    'Staff': {
        'fpiweb': {
            'activity': [
                'view_activity',
            ],
            'box': [
                'print_labels_box',
            ],
            'constraints': [
                'add_constraints',
                'change_constraints',
                'delete_constraints',
                'view_constraints',
            ],
            'locbin': [
                'add_locbin',
                'change_locbin',
                'delete_locbin',
                'view_locbin',
            ],
            'locrow': [
                'add_locrow',
                'change_locrow',
                'delete_locrow',
                'view_locrow',
            ],
            'loctier': [
                'add_loctier',
                'change_loctier',
                'delete_loctier',
                'view_loctier',
            ],
            'profile': [
                'view_system_maintenance',
            ],
        },
    },
}


def iterate_permissions(permissions):
    for app_label, models in permissions.items():
        for model, model_permissions in models.items():
            for permission in model_permissions:
                yield app_label, model, permission


def setup_group_permissions(group, permissions):

    print(f"Clearing {group.name} permissions.")
    group.permissions.clear()

    for app_label, model, codename in iterate_permissions(permissions):
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






