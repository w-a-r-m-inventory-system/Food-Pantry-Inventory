#!/usr/bin/env python

# Boilerplate for stand-alone Django scripts
from django import setup
setup()

# ---------------------------------------------------------

from django.contrib.auth.models import Group
from django.db.models import Q

criteria = Q(name__istartswith='volunteer')
criteria |= Q(name__istartswith='staff')
criteria |= Q(name__istartswith='admin')

for group in Group.objects.filter(criteria):
    print(repr(group.name))

    permissions = group.permissions.values_list(
        'content_type__app_label',
        'content_type__model',
        'codename'
    ).order_by(
        'content_type__app_label',
        'content_type__model',
        'codename'
    )

    for app_label, model, codename in permissions:
        print(
            "({}, {}, {}),".format(
                repr(app_label),
                repr(model),
                repr(codename),
            )
        )









