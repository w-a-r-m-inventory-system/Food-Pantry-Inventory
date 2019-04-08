"""
WSGI config for FPIDjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FPIDjango.settings')

application = get_wsgi_application()
