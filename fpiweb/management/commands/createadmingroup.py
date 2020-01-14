
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError

# Custom django-admin / manage.py command as per
# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/


class Command(BaseCommand):

    help = """Create an admin group for the fpiweb app."""

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--force',
            action='store_true',
            help="If group already exists, reset all permissions",
        )
        parser.add_argument(
            'groupname',
            metavar='GROUPNAME',
            nargs=1,
            type=str,
            help="Name of group to add or edit",
        )

    def handle(self, *args, **options):
        group_name = options.get('groupname')[0]
        force = options.get('force', False)

        group, created = Group.objects.get_or_create(name=group_name)
        if not created:
            if not force:
                message = f"group {group_name} already exists and -f/--force option not specified"
                raise CommandError(message)
            print(f"clearing group {group_name}'s permissions")
            group.permissions.clear()

        fpiweb_permissions = Permission.objects.filter(
            content_type__app_label='fpiweb',
        )

        box_type_permissions = fpiweb_permissions.filter(
            content_type__model='boxtype',
            codename__in=(
                'add_boxtype',
                'change_boxtype',
                'delete_boxtype',
                'view_boxtype',
            )
        )
        for permission in box_type_permissions:
            group.permissions.add(permission)