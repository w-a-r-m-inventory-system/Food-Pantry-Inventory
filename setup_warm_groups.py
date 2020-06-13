#!/usr/bin/env python

"""
setup_warm_groups.py - Establish the groups and permissions for WARM users.

Overview and Group Definitions
------------------------------

This program sets up the group and their permissions for the WARM
database.  WARM is expected to have three levels occess to use this system.

Volunteer
    Most users will have this level.  It allows the user to
    checkin and out boxes of product into the system.

Staff
    Staff users can create and manage volunteer and staff users, as well as
    manage the application data such as product, category, location,
    etc.  They also have all the privileges of a volunteer.

Admin
    Admin users are Django superusers.  They can manage any table in the
    database directly via the Django admin web interface.  In addition to
    having all the privileges of a staff user, the application provides the
    ability to add and manage other admins.

Requirements
------------

This program will not work as expected until the migration
0029_add_model_permissions.py has been applied to the database.

In turn, this program must be run before the application will work properly.
"""
from typing import Dict, List
from sys import stderr

# ---------------------------------------------------------

if __name__ == '__main__':

    # Boilerplate for stand-alone Django scripts

    from django import setup
    setup()

    from django.contrib.auth.models import Group, Permission


    GROUPS_AND_PERMISSIONS: Dict[str, Dict[str, Dict[str, List[str]]]] = {
        'Volunteer': {
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
        """
        Generator to pick up the needed foreign keys for a given permisison.

        :param permissions: attributes associated with this permission
        :return:
        """
        for app_label, models in permissions.items():
            for model, model_permissions in models.items():
                for permission in model_permissions:
                    yield app_label, model, permission


    def setup_group_permissions(group, permissions):
        """
        For a given group, create or replace the permisisons for it.

        :param group: group to be created or replaced
        :param permissions: list of permissions to be applied to this group
        :return:
        """

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
        """
        Create or replace groups and add permissions.

        :param groups_and_permissions: table of groups and associated permissions
        :return:
        """
        for group_name, permissions in groups_and_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                print(f"Created {group_name} group.")
            else:
                print(f"Found {group_name} group.")

            setup_group_permissions(group, permissions)
            print()

    # run application
    setup_groups_and_permissions(GROUPS_AND_PERMISSIONS)

# EOF
