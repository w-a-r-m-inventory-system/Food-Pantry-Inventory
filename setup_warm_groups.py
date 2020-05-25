#!/usr/bin/env python

# Boilerplate for stand-alone Django scripts
from django import setup
setup()

# ---------------------------------------------------------

from sys import stderr

from django.contrib.auth.models import Group, Permission


fpiweb_permissions = Permission.objects.filter(
    content_type__app_label='fpiweb'
)

queryset = fpiweb_permissions.filter(
    content_type__model='box',
).values_list(
    'content_type__model',
    'codename'
)
print(queryset)
print()

group_name = 'Volunteers'
group, created = Group.objects.get_or_create(name=group_name)
if created:
    print(f"Created {group_name} group.")
else:
    print(f"Found {group_name} group.")

print(f"Clearing {group_name} permissions.")
group.permissions.clear()

model_codename_pairs = (
    ('pallet', 'build_pallet'),
    ('box', 'add_box'),
)

for model, codename in model_codename_pairs:
    try:
        permission = fpiweb_permissions.get(
            content_type__model=model,
            codename=codename
        )
    except Permission.DoesNotExist:
        print(f"Permission {model} {codename} not found", file=stderr)
        continue

    print(f"Granting {model} {codename} to {group_name}")
    group.permissions.add(permission)








