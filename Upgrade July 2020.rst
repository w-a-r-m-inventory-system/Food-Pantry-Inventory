*******************************
Upgrade July 2020 - Quick Notes
*******************************

Permissions
===========

The big change to the system is the implementation of permissions.  There
are three permission levels: Volunteer, Staff, and Admin.

Volunteers have access to:

-   Add new boxes to the system
-   Check the status of any box
-   Fill, move, and consume (empty) boxes
-   Fill and move pallets of boxes
-   Login, change their password, and logout
-   See the "About" screen

Staff users have access to:

-   Everything a volunteer can do
-   The system maintenance menu (where they can add or update users
-   Print pages of labels
-   Download the activity log (csv)
-   Use the Django admin menu to arbitrarily update data in the application
    tables

Admin users have access to:

-   Everything a Staff person can do
-   Full access to the Django admin menu

In order to implement these changes, the following steps must be done.

1.  Upgrade the libraries (see `Library Changes`_ below).
2.  Apply a database migration (see `Database Changes`_ below).
3.  Make changes to the Django permission tables (see `Implement
    Permissions`_ below).
4.  Login as yourself (assuming that your user ID has superuser privileges).
5.  Go to the system manintenance -> user maintenance menu pick and add some
    users with various permission levels noted above.
6.  Test


Database Changes
================

To apply the databasse changes run the following command:

    ./manage.py migrate

Implement Permissions
=====================

To apply the changes to the Django permissions tables do run the following:

    ./python setup_warm_groups.py

Using uWSGI and Nginx
=====================

Nginx
-----

Nginx is installed outside of the project.  It has a configureation file
that tells it where things are and what port to expect incoming web requests
and what port uWSGI is listening for reequests.

uWSGI
-----

uWSGI is installed in the project and run from there in the setup I put
together.  Other platform install uWSGI as a service that is managed by the
operating system.

Menu Restructuring
==================

The menus have been simplified.  A volunteer only sees the menu choices she
is able to use.  Staff and admins see an additional system management
section that allows them to get to the rest of the menu system.

Library Changes
===============

A number of libraries have been added or upgraded.
Please update your requirements by running::

    pip install -r requirements.txt

There are some libraries that may not load -- especially if your platform
is Windows.  For development some libraries are not needed.  Others are
needed only for testing certain aspects of testing or deployment.  If pip
fails to load any of the following libraries, just delete that line from the
requirements.txt file and rerun pip.

=========================   =============================
Library                     What cannot be tested or used
=========================   =============================
uWSGI                       Needed only for testing deployment
selenium                    Needed only for two of the modules in the test
                            directory
geckodriver-autoinstaller   Needed only for selenium
gunicorn                    a possible replacement for uWSGI
=========================   =============================

Possible Problems and Bugs
==========================

These items will probably be added to the issues list on github or speedily
fixed.

-   Change password is not yet implemented.

-   It is possible tht staff folks cannot actually get into the Django admin
    section.

-   Some of the validation is still missing

    -   Password validation is not yet implemented and tested
    -   Email validation has not yet been tested

-   Pytest modules for the permissions still needs to be written

-   Nginx support needs to be documented

-   uWSGI support needs to be documented

