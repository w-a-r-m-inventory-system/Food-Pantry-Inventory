:orphan:

*****************
Django Guidelines
*****************

This document discusses how to use Django without requiring the Professoinal
version of PyCharm.

Setup
=====

In addition to updating your local and public git repositories to include
recent pull requests, there are several other configuration steps that need
to be taken.

Create New Run Configuration
----------------------------

Create a "Pure Python" run configuration (with the menu Run -> Edit
Configuration with the following properties:

+--------------+------------------------------+-------------------------------+
|Property      | Value                        | Comment                       |
+==============+==============================+===============================+
| Name:        | Run Django Manually          | This is arbitrary.  Use what  |
|              |                              | you like.                     |
+--------------+------------------------------+-------------------------------+
| Script path: | <project directory>/manage.py| This is the special program   |
|              |                              | that Django used to do its    |
|              |                              | magic.                        |
+--------------+------------------------------+-------------------------------+
|Parameters:   | runserver localhost:8765     | This tells Django we run the  |
|              |                              | server on our own machine on  |
|              |                              | port 8765                     |
+--------------+------------------------------+-------------------------------+
|Environment   | DJANGO_SETTINGS_MODULE=      | This tells Django where to    |
|variables:    | FPIDjango.private            | look for your private         |
|              |                              | configuration file.           |
+--------------+------------------------------+-------------------------------+
|Working       | <project directory>/work     | If you haven't created this   |
|Directory:    |                              | directory yet, please do so   |
|              |                              | now.                          |
+--------------+------------------------------+-------------------------------+
|Add content roots to PYTHONPATH  checked     |                               |
+---------------------------------------------+-------------------------------+
|Add source roots to PYTHONPATH   checked     |                               |
+---------------------------------------------+-------------------------------+

After this configuration has been created, save it for later use.

Configure PostgreSQL Server
---------------------------

Install PostgreSQL according to the instructions given in the document
:doc:`PostgreSQL Guidelines <PostgreSQLGuidelines>`.

When finished with the installation and configuration of PostgreSQL, there
should be a running server on your local computer with a database named
**WARM** in it.

Tailor Django Access
--------------------

Find the the file <project>/FPIDjango/settings.py and make the following
changes:

#.  Make a directory called <project>/FPIDjango/private.

#.  Copy the file settings_private.py into the new private
    directory.

#.  Edit the file settings_private.py in the private directory to match your
    database values.

#.  Change the value for MY_SECRET_KEY to some 50 character random value in
    the new settings_private.py.

Run Django
==========

To run Django (without the professional version of PyCharm), perform these
steps:

#.  Verify that the PostgreSQL server is running.

#.  Execute the run configuration created in `Create New Run Configuration`_
    above.

#.  After it starts up, it will display a link in the window of the **Run**
    tab at the bottom.  You may have to click on that tab to get it to display.

#.  Instead of going there in the browser, go to http://localhost:8765/fpiweb.

#.  Until we add real code, the browser will display a one line hello message.

#.  When finished, click on the red box on the left edge of the Run window
    to stop the Django web server.

Manage Django
=============

As the application moves from conception to production, Django has varous
tools to assist the development of the application.

Database Management
-------------------

As is widely known, one of the major features of Django is the ORM (Object
Relational Model which is used for automating the relationship between the
Python code and the database.

Preliminary Setup
-----------------

Django has some internal tables it will need to setup in the database.
These tables include administering credentials for authorized users and
managing sessions.  To prepare for this, do the following:

#.  Temporarily block Django from seeing our code by commenting out line 36
    in FPIDjango/settings.py.  It should look like:

    ::

            # 'fpiweb.apps.FpiwebConfig',

#.  Temporarily use the default templating system that comes with Django by
    uncommenting line 60 and commenting line 61 so it looks like this:

    ::

        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'BACKEND': 'django.template.backends.jinja2.Jinja2',


#.  Prepare for the most current Django tables.

    ::

        python3 manage.py migrate

    At this point the tables in the database that Django needs have been
    created.

#.  Create a superuser account (to administer the database).

    ::

        python3 manage.py createsuperuser

    This will ask you for a username, an email address and a password (twice).

#.  Test this by starting the server and going to the following URL.

    ::

        http://localhost:8765/admin/

    A login page will be presented.

#.  Login with the credentials created two steps above.

#.  Create another user for your system.

#.  Uncomment our application at line 36 in FPIDjango/settings.py.  It
    should look like:

    ::

            'fpiweb.apps.FpiwebConfig',

#.  Leave the templating set to the Django default for now.

Development Interactions
========================

Developers interact with Django in a number of ways.

Table Models
------------

For each table desired in the database, a "model" is coded.  The model tells
Django the name of the table, the name of the fields, and the field attributes.

Once a model is defined for a table, Django can create the actual table in
the database from it.  The following steps are used to create the table.

#.  Tell Django to look for new or revised models:

    ::

        python3 manage.py makemigrations fpiweb

    This builds the SQL commands that Django will run in a later step.  Note
    the four digit prefix for the migration file created.

#.  View the proposed SQL commands the Django will run to propagate the
    change to the database for this migration.

    ::

        python3 manage.py sqlmigrate fpiweb <migration number>

        <migration number> is the four digit number noted in the prevous step.

    Review the SQL statement(s) to verify that the additions and changes you
    desire will be correctly propagated to the database.

#.  Verify that Django hasn't found a problem with our changes to the
    database.

    ::

        python3 manage.py check

    If any problems are found, correct them before continuing.

#.  Apply model changes to the database.

    ::

        python3 manage.py migrate

    Verify the schema changes with pgAdmin 4 or a tool of your choice.


