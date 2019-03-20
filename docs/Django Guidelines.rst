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
|Environment   | DJANGO_SETTINGS_MODULE=      | This tells Django where to    |
|variables:    | FTPDjango.settings           | look.                         |
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
:doc:`PostgreSQL Guidelines <PostgreSQL Guidelines>`.

When finished with the installation and configuration of PostgreSQL, there
should be a running server on your local computer with a database named
**WARM** in it.

Tailor Django Access
--------------------

Find the the file <project>/FPIDjango/settings.py and make the following
changes:

#.  Find the section starting with **"DATABASES"** (currently at line 79).

#.  Comment out the three lines following that reference a "default" sqlite
    database.

#.  Uncomment the lines describing access to the PostgreSQL server
    (currently lines 84 through 91).

#.  Modify the parameters for accessing the PostgreSQL server.  In
    particular change the values for:

    -   USER - this is the userid for the database administrator.

    -   PASSWORD - this is the password for the same user given above.

    -   PORT - change as needed if you had to install PostgreSQL using a
        non-default port.

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
