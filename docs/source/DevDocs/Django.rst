:orphan:

**************
Django Support
**************

Django support has been added to this project.  A revised
requirements.txt file has been included in this change.

Files and Directories
#####################

    -   manage.py - this script has been added to the main
        directory to run the Django server in development mode.
        Production will use a different arrangement.

    -   FPIDjango directory - This directory contains all the
        Django code, settings, and configuration files.  All of
        the "front-end" code will live in subdirectories of this
        directory.

How to Run
##########

#.  Create a new run configuration

    -   Name - Call it whatever you want, e.g. "Run Django Server".

    -   Parameters - "runserver localhost:<port>"  where
        <port> can be any number between 8000 and 9000.

    -   Environment varibles - add the environment variable
        DJANGO_SETTINGS_MODULE with the value FPIDjango.settings.

    -   Working directory - set to the work subdirectory.

    -   Add content roots to PYTHONPATH - Should be checked.

    -   Add source roots to PYTHONPATH - Should be checked.

#.  Save run configuration.

#.  Run it. If configured correctly, there will be messages in the Run tab
    about how it started and is accessable via a browser on localhost at the
    port specified.

#.  Start a browser and go to the port indicated.  There should be a
    Django page displayed.

