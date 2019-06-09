*****************
Outstanding Tasks
*****************

There are numerous tasks and activities that remain to be accomplished by
someone before this project can be deployed.

This task table shows all the known activities that remain to be done.  The
details of each task are given below.

Task Table
==========

..  table::  Task Table
    :widths: auto
    :align: left

    =======  ========  =======  ==============================================
    Task ID  Priority  Issue #  Title
    =======  ========  =======  ==============================================
    `T1`_              55       QR Label print program needed
    `T2`_              54       Product Examples Table
    `T3`_              53       Modify base.html template to use static files
    `T4`_              42       Box Type Table
    `T5`_              41       Product Table
    `T6`_              40       Product Category Table
    `T7`_              39       Build Add Inventory Screen
    `T8`_              56       Add ability to move a box
    `T9`_              57       Scan a QR code
    `T10`_             58       Getting error from autodoc when running Sphinx to create documentation
    =======  ========  =======  ==============================================


Task Descriptions
=================

.. _T1:

**T1: QR Label print program needed**
-------------------------------------

This program can be standalone.  It does not need to be incorporated into
the Django framework.

Purpose
+++++++

Print a page of QR codes on plain 8 1/2" by 11" paper.

Details
+++++++

Requirements:

-   The QR codes need to be at least 2 inches square.

-   Each QR code should contain a URL that has the format:

    -   https://<domain>/fpiweb/box/<box-id>

    where

    -   <domain> is (for now) a value passed in on the command line.

    -   <box-id> is a nine character string of "boc" followed by a six digit
        decimal number.

    example (<domain> = www.example.com and <box-id> = box123456

    -   /https://www.example.com/fpiweb/box/box123456

-   In addition, each QR code should have the box number printed immediately
    below it and centered with the QR code..

    example:

::

                          xxxxxxxxxxxxxxxxx
                          xxxxxxxxxxxxxxxxx
                          xxxxxxxxxxxxxxxxx
                          xxxxxxxxxxxxxxxxx
                          xxxxxxxxxxxxxxxxx
                          xxxxxxxxxxxxxxxxx
                              BOX123456

-   The QR codes can be printed several times across the page, but there
    should be at least a one/fourth inch white space gap on all sides.

-   The QR codes pages should be printed on only one side.

-   The box numbers to be printed are selected as follows:

    -   The beginning of the box numbers will be specified on the command line.

    -   The number of QR codes to be printed will be speciified on the
        command line.

    -   The box numbers will be printed in ascending order.

    -   The actual box numbers printed will be based on the box numbers
        already contained in the database.

        -   Any box number already in the database will be skipped.

        -   It does not matter if the box number in the database is empty or
            full.  It is presumed to be affixed to a box already.

-   This program will not modify the database. I.e. although it is preparing
    labels for the boxes, the box numbers will not be added to the database
    until the the QR code is scanned later.

.. _T2:

**T2: Product Examples Table**
------------------------------

Build web pages that will allow an authorized user to add, change and delete
product example entries.  Each product example entry must be associated
with one (and only one) product.  Changing a product example entry will
include changing which product is associated with it.

.. _T3:

**T3: Modify base.html template to use static files**
-----------------------------------------------------

Currently, when the we site is first presented to the user, the code
downloads the bootstrap css and javascript.  The code needs to be changed so
that any css and javascript are already stored in the static files and
folders in the Django instance so there no need to access any other sites
on the web when using our application.

.. _T4:

**T4: Box Type Table**
----------------------

Build web pages that will allow an authorized user to add, change and delete
box type entries.  Deleting a box type will not be permitted
if there are any product entries referencing this box type.

.. _T5:

**T5: Product Table**
---------------------

Build web pages that will allow an authorized user to add, change and delete
product entries.  Each product entry must be associated with one (and only
one) product category.  Changing a product entry will include changing which
product category is associated with it.  Deleting a product entry will be
permitted only if no product example entries are associated with it.

.. _T6:

**T6: Product Category Table**
------------------------------

Build web pages that will allow an authorized user to add, change and delete
product category entries.  Deleting a product category will not be permitted
if there are any product entries referencing this product category.

.. _T7:

**T7: Build Add Inventory Screen**
----------------------------------

Build web pages to add inventory to the system.

Requirements:

-   If the box number is not already in the box table, add this box entry to
    the table when saved.

-   If the box number is already in the box table and is empty (no product),
    prepopulate the box type from the box record found.

-   If the box type is not prepopulated, default to the "Evans" box type.

-   If the box number is already in the box table and is not empty (some
    product is currently in the record, show an error message and allow
    the user to empty the box before continuing.

-   Validate the fields as needed (product, expiration year),

-   Allow the user to specify beginning and ending months if the user
    desires.  Entering a month in either field requires that the other must
    be filled.  However, allow the user the option to blank out both fields,
    if desired.

-   When saved, create a new activity record and fill in these fields from
    the new box record just saved.

    -   box number
    -   box type
    -   date_filled
    -   exp_month_start (use 1 unless otherwise specified in the box record)
    -   exp_year
    -   loc_row
    -   loc_bin
    -   loc_tier
    -   product_cat_name (string not product category id)
    -   prod_name (string not product id)
    -   quantity (from box type record)

.. _T8:

**T8: Add ability to move a box**
---------------------------------

Build web pages to move a box from one location to another.  Validate that
the box is in inventory and already filled with product.  Also validate that
the location to which the box is being moved.

This function will find the appropriate activity record and modify it by
changing the location.

.. _T9:

**T9: Scan a QR code**
----------------------

Build a screen that is presented when a QR code has been scanned.  Based on
what is found or not found in the database, switch to an appropriate screen.

..  table::  Box Record Status and Action Taken
    :widths: auto
    :align: left

=================  ============
Box Record Status  Action Taken
=================  ============
No box record      Present new box screen
Box record empty   Present new box screen
Box record filled  Present empty or move box screen
=================  ============

.. _t10:

**T10: Getting error from autodoc when running Sphinx to create documentation**
-------------------------------------------------------------------------------

Getting the following error when running Sphinx.

::

    WARNING: autodoc: failed to import module 'views' from module 'fpiweb'; the following exception was raised:
    Traceback (most recent call last):
    File "/Volumes/MBPC/Dvl/Python/PythonProjects/Food-Pantry-Inventory/venv/lib/python3.7/site-packages/sphinx/ext/autodoc/importer.py", line 232, in import_module
        __import__(modname)
    File "/Volumes/MBPC/Dvl/Python/PythonProjects/Food-Pantry-Inventory/fpiweb/views.py", line 14, in <module>
        from django.contrib.auth.mixins import LoginRequiredMixin
    File "/Volumes/MBPC/Dvl/Python/PythonProjects/Food-Pantry-Inventory/venv/lib/python3.7/site-packages/django/contrib/auth/mixins.py", line 3, in <module>
        from django.contrib.auth.views import redirect_to_login
    File "/Volumes/MBPC/Dvl/Python/PythonProjects/Food-Pantry-Inventory/venv/lib/python3.7/site-packages/django/contrib/auth/views.py", line 10, in <module>
        from django.contrib.auth.forms import (
    File "/Volumes/MBPC/Dvl/Python/PythonProjects/Food-Pantry-Inventory/venv/lib/python3.7/site-packages/django/contrib/auth/forms.py", line 10, in <module>
        from django.contrib.auth.models import User
    File "/Volumes/MBPC/Dvl/Python/PythonProjects/Food-Pantry-Inventory/venv/lib/python3.7/site-packages/django/contrib/auth/models.py", line 3, in <module>
        from django.contrib.contenttypes.models import ContentType
    File "/Volumes/MBPC/Dvl/Python/PythonProjects/Food-Pantry-Inventory/venv/lib/python3.7/site-packages/django/contrib/contenttypes/models.py", line 133, in <module>
        class ContentType(models.Model):
    File "/Volumes/MBPC/Dvl/Python/PythonProjects/Food-Pantry-Inventory/venv/lib/python3.7/site-packages/django/db/models/base.py", line 111, in __new__
        "INSTALLED_APPS." % (module, name)
    RuntimeError: Model class django.contrib.contenttypes.models.ContentType doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.

