#!/usr/bin/env python

# ---------------------------------------------------------
if __name__ == '__main__':

    # Boilerplate for stand-alone Django scripts
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FPIDjango.settings')

    from django import setup
    setup()

    from django.contrib.auth.models import Group
    from django.db.models import Q

    criteria = Q(name__istartswith='volunteer')
    criteria |= Q(name__istartswith='staff')
    criteria |= Q(name__istartswith='admin')

    with open('perms.txt', mode='w') as outfile:
        for group in Group.objects.filter(criteria):
            print(repr(group.name), file=outfile)

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
                    ), file=outfile
                )

# EOF
