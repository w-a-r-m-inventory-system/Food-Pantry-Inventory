"""
settings_private.py - Shadow or pseudo-private file.

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

# The name of the engine Django needs to use to access the database
DB_ENGINE = "django.db.backends.postgresql"

# The name of your database
DB_NAME = "WARM"

# The user ID to be used by Django to accss the database.
DB_USER = "postgres"

# The password for this user
DB_PSWD = "PSWD"

# The host for the database server
DB_HOST = "localhost"  # can also be '127.0.0.1'

# The port used by the database server
DB_PORT = "5432"


# Specify any additonal private parameters here.
MY_SECRET_KEY = "<specify your own random  string of 50 characters>"

# This snippet of code can be used to generate a random secret key
# from string import printable
# from datetime import datetime
# from random import choice, seed
# seed(datetime.now().microsecond)
# "".join([choice(printable) for i in range(50)])

# EOF
