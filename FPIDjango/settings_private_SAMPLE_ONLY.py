"""
settings_private_SAMPLE_ONLY.py - Shadow or pseudo-private file.

This file has dummy settings in it.  The purpose is to show the format of
your real settings_private file in the private subdirectory.

The files at this level are dummy files that are safe to upload to GitHub.
The equivalent files in the private subdirectory are ignored by git so it
is safe to put your sensitive (and really private) parameters in those files.

When you run Django on your system for real, change the environment
variable for DJANGO_SETTINGS_MODULE from FPIDjango.settings to
FPIDjango.private.settings.
"""

__author__ = "(Multiple)"
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"

import os

# Turn debugging on (= 1) or off (= 0)

DEBUG_SETTING = os.environ.get(
    "DEBUG",
    default=True
)


# The name of the engine Django needs to use to access the database
DB_ENGINE_SETTING = os.environ.get(
    "SQL_ENGINE",
    default='django.db.backends.postgresql'
)

# The name of your database
DB_NAME_SETTING = os.environ.get(
    "SQL_DATABASE",
    default='WARM'
)

# The user ID to be used by Django to accss the database.
DB_USER_SETTING = os.environ.get(
    "SQL_USER",
    default='postgres'
)

# The password for this user
DB_PSWD_SETTING = os.environ.get(
    "SQL_PASSWORD",
    default='PSWD'
)

# The host for the database server
DB_HOST_SETTING = os.environ.get(
    "SQL_HOST",
    default='localhost'
)   # can also be # '127.0.0.1'

# The port used by the database server
DB_PORT_SETTING = os.environ.get(
    "SQL_PORT",
    default='5432'
)

# location for a copy of all the static files on this computer\
STATIC_ROOT_SETTING = os.environ.get(
    "DJANGO_STATIC_ROOT",
    default='<static root directory'
)

ALLOWED_HOSTS_SETTING = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    default='localhost'
).split()

# Specify any additonal private parameters here.
SECRET_KEY_SETTING = os.environ.get(
    "SECRET_KEY",
    default='<specify your own random string of 50 characters>'
)
# To generate your own random string, run
#    python StandaloneTools/GenerateSecretKey.py

# and paste the generated string wherever needed.

# or use this snippet of code to generate a random secret key
# from string import printable
# from datetime import datetime
# from random import choice, seed
# seed(datetime.now().microsecond)
# "".join([choice(printable) for i in range(50)])

# EOF
