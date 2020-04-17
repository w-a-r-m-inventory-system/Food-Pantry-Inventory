*****************
Outstanding Tasks
*****************

There are numerous tasks and activities that remain to be accomplished by
someone before this project can be deployed.

This task table shows all the known activities that remain to be done.  The
details of each task are given below.  As tasks are completed the
details will be moved to an appropriate location elsewhere in this
documentation.

Task Table
==========

..  table::  Task Table
    :widths: auto
    :align: left

    ========  =========  ====================================================
    Issue #   Milestone  Title
    ========  =========  ====================================================
    `I-202`_  `M-V0.9`_  blah blah
    `I-201`_  `M-V1.0`_  blah blah
    `I-200`_  `M-V1.1`_  blah blah
    `I-199`_  `M-ReWk`_  blah blah
    `I-198`_  `M-V0.9`_  Build Pallet Screen Enhancement
    `I-192`_  `M-V0.9`_  Build Pallet Screen. Save more in Pallet Box record
    `I-190`_  `M-V0.9`_  Build Pallet: set pallet ID in profile
    `I-189`_  `M-V0.9`_  Ensure that the "Evans" box type is default
    `I-178`_  `M-V0.9`_  Manual box checkin needs to be streamlined
    `I-177`_  `M-V0.9`_  Add start/end months to Manual Box Checkin
    `I-176`_  `M-V0.9`_  Change user password
    `I-175`_  `M-V0.9`_  Add/Change/Delete a User
    `I-174`_  `M-V0.9`_  Delete a pallet
    `I-173`_  `M-V0.9`_  Build Pallet needs to set pallet status
    `I-167`_  `M-V0.9`_  Results of Mike R.'s original testing
    `I-165`_  `M-V0.9`_  Automatically add a profile when needed
    `I-161`_  `M-V0.9`_  Move Pallet
    `I-145`_  `M-V0.9`_  Defaults for start/end month won't go back to zero
    `I-139`_  `M-V0.9`_  Build Pallet Screen: Navigation and Pallet records
    `I-138`_  `M-V0.9`_  Enhance README.md with a more detailed purpose.
    `I-125`_  `M-V0.9`_  Add/Move box(es) should merge into location.
    `I-124`_  `M-V0.9`_  Manual pallet and box management
    `I-115`_  `M-V0.9`_  Rework the API of theQR label print program
    `I-89`_   `M-V0.9`_  Improve README.md etc. for easier for joining.
    `I-88`_   `M-V0.9`_  Make a docker file and image of project to run locally
    `I-71`_   `M-V0.9`_  QR Print Label Program - GUI Version Needed
    `I-64`_   `M-V0.9`_  Populate Box.quantity when Box record is created.
    `I-54`_   `M-V0.9`_  Product Examples Table - Build A/C/D screens
    `I-42`_   `M-V0.9`_  Box Type Table - Build A/C/D screens
    `I-41`_   `M-V0.9`_  Product Table - build A/C/D screens
    `I-40`_   `M-V0.9`_  Product Category Table - build A/C/D screens
    ========  =========  ====================================================

Milestone Descriptions
======================

_`M-V0.9`  Version 0.9 Pre-production demo

_`M-V1.0`  Version 1.0 - MVP

_`M-V1.1`  Version 1.1 First polish

_`M-ReWk`  Needs to be reworked.

Task Descriptions
=================

    _`I-202`  blah blah
    _`I-201`  blah blah
    _`I-200`  blah blah
    _`I-199`  blah blah
    _`I-198`  Build Pallet Screen Enhancement
    _`I-192`  Build Pallet Screen. Save more in Pallet Box record
    _`I-190`  Build Pallet: set pallet ID in profile
    _`I-189`  Ensure that the "Evans" box type is default
    _`I-178`  Manual box checkin needs to be streamlined
    _`I-177`  Add start/end months to Manual Box Checkin
    _`I-176`  Change user password
    _`I-175`  Add/Change/Delete a User
    _`I-174`  Delete a pallet
    _`I-173`  Build Pallet needs to set pallet status
    _`I-167`  Results of Mike R.'s original testing
    _`I-165`  Automatically add a profile when needed
    _`I-161`  Move Pallet
    _`I-145`  Defaults for start/end month won't go back to zero
    _`I-139`  Build Pallet Screen: Navigation and Pallet records
    _`I-138`  Enhance README.md with a more detailed purpose.
    _`I-125`  Add/Move box(es) should merge into location.
    _`I-124`  Manual pallet and box management
    _`I-115`  Rework the API of theQR label print program
    _`I-89`  Improve README.md etc. for easier for joining.
    _`I-88`  Make a docker file and image of project to run locally
    _`I-71`  QR Print Label Program - GUI Version Needed
    _`I-64`  Populate Box.quantity when Box record is created.
    _`I-54`  Product Examples Table - Build A/C/D screens
    _`I-42`  Box Type Table - Build A/C/D screens
    _`I-41`  Product Table - build A/C/D screens
    _`I-40`  Product Category Table - build A/C/D screens

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

    -   <box-id> is a nine character string of "BOX" followed by a five digit
        decimal number.

    example (<domain> = www.example.com and <box-id> = box123456

    -   /https://www.example.com/fpiweb/box/BOX12345

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
if there are any box entries referencing this box type.

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
