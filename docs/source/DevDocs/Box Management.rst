########################
Box and Activity Summary
########################

This food pantry inventory system tracks the food and other product in
the warehouse by box.  When a box has product in it, the system tracks
what is in the box, where the box is located, and when the product in it
will expire.

The system also tracks box activity.  The activity information is
designed to help the folks running the food pantry understand the flow
of product through the pantry over time.  This information can help them
see the trends of their clients.  They can anticipate when they are
about to run low or when they have an excess of some product that
another food pantry can use before it expires and has to be thrown away.


***********
Box Summary
***********

All boxes have a box type -- which indicates an approximate quantity of
product it might contain.  All boxes have a QR code label with a unique
identifier included for humans to read.  The QR code can be easily read
by devices such as smart phones, tablets and laptops with cameras.

A box may be either empty or full in the inventory system.  Scanning the
QR code or typing in the identifier into the appropriate web page will
reveal the state of the box in the system.

A full box in the inventory system has information about what product is
in it, where it is located, and when the product in it will expire.  The
expiration information may indicate the only the year it expires or may
indicate a part of a year, such as a quarter or month.  If a box is
moved, the system is updated so finding the current location of any box
is known.

An empty box will have nothing but the box type.  The inventory system
will have no product, location, or expiration information.  However, the
boxes are expected to be sufficiently durable that they can be used a
number of times.

****************
Activity Summary
****************

When a box has product in it, the activity information will also have
the product, approximate quantity, location and expiration information
about that box.  When a box is consumed (i. e. emptied) the activity
information will be updated to indicate when it was consumed, how long
the product was in the box, etc.  When a box is used again, a new
activity record will be created so the information about the previous
contents is preserved.

**************
Box Management
**************

Ideally all boxes are handled correctly so this inventory system can
accurately report the quantity and location of all products in it.

Alas, we all know that mistakes can be made.  A box may get overlooked
and not get checked in.  A box may get moved without letting the
inventory system know.  A box may get emptied by someone who is unaware
that there is an inventory system.  The inventory system is tolerant of
these foibles and tries to compensate rather than be rigid and require
extra work.

The management of updating the database after user interaction has been
isolated to two classes: BoxManagementClass and BoxActivityClass.  These
two classes should be the only code actually updating  the database.
Additional guidance is provided below in the section `Pallet
Management`_ about how pallets of boxes are handled by this inventory
system.


Box Management API Summary
==========================

The `BoxManagementClass`_ has five API's or public methods that can be
called to update the database with details about a box (or a pallet of
boxes).

Individual Box API's
---------------------

For individual boxes the calls are:

BoxManagementClass.box_new
    Add a new box with a unique number to the inventory system.  It will
    also have a predefined box type to indicate approximately how many items
    (cans, boxes, packages, etc.) are in the box.

BoxManagementClass.box_fill
    Fill an individual box with a named product at a specified location
    with a specified expiration year (and possibly range of months).

BoxManagementClass.box_move
    Move a filled box from one location to another in the warehouse.

BoxManagementClass.box_consume
    Empty a box (consume it's contents) by putting the contents into QC or
    directly in the pantry.


Box Management API Details
==========================

The expected input, actions, and output of the box management API calls are
shown below.

BoxManagementClass.box_new
--------------------------

Add a new box with a unique box number to the inventory system.

Expected Input
^^^^^^^^^^^^^^

A unique box number and a valid box type.

Action
^^^^^^

A box record will be added to the inventory with the supplied box type.  All
other fields in the box will be empty.

Output
^^^^^^

The new box record will be returned.

BoxManagementClass.box_fill
---------------------------

Add an individual box containing a named product at a specified location
with a specified expiration year (and possibly range of months).

Expected Input
^^^^^^^^^^^^^^

The unmodified box record and the information needed to update the box.

Actions
^^^^^^^

This API call will mark the indicated box with the contents, location and
expiration indicated.  It will also make the call to create the appropriate
Activity record.

Output
^^^^^^

The modified box record will be returned.


BoxManagementClass.box_move
---------------------------

Move a filled box from one location to another in the warehouse.

Expected Input
^^^^^^^^^^^^^^

The unmodified box record and the target location.

Actions
^^^^^^^

This API call will change the location in the box record to the new
location specified. It will also make the call to create the appropriate
Activity record.

Output
^^^^^^

The modified box record will be returned.


BoxManagementClass.box_consume
------------------------------

Empty a box (consume it's contents) by putting the contents into QC or
directly in the pantry.

Expected Input
^^^^^^^^^^^^^^

The unmodified box record.

Actions
^^^^^^^

This API call will make the call to create the appropriate Activity record.
It will then clear all the product, location, and expiration fields in the
box record.

Output
^^^^^^

The modified box record will be returned.

*****************
Pallet Management
*****************

Pallet management is designed to make dealing with pallets of boxes swift
and easy.  Rather than require strict conformance to some arbitrary rules in
the inventory system, the system will accommodate variations to the typical
scenarios.  The scenarios below are not meant to be inclusive but are
designed to show developers what might happen.


Pallet Management Scenarios
===========================

New Pallet Scenario
    The user will start with an empty pallet and add newly filled boxes of
    product to it.  When the pallet is full or there are no more newly
    filled boxes, a location is selected and (after scanning the QR codes
    and filling in the pallet box info) the pallet is placed in the new
    location.

    Variation:  The user decides to take similarly packed boxes from another
    pallet and add them to this pallet.  The system will recognize that
    these boxes were originally somewhere else and will process them as a
    move.

Add to a Pallet Scenario
    The user will pull a pallet out of the racks and add newly filled boxes
    to it.  After scanning the QR codes and filling in the pallet box info
    for the boxes just added, the user puts the pallet back in the racks at
    the same location.

    Variation 1:  The user decides to take similarly packed boxes from another
    pallet and add them to this pallet.  The system will recognize that
    these boxes were originally somewhere else and will process them as a
    move.

    Variation 2:  The user accidentally scans the QR code for a box that was
    already on the pallet.  As long as the product and expiration
    information are the same, the system will ignore the entry.

    Variation 3:  The user decides to put the pallet in a different
    location.  As long as all the boxes are scanned, when the finished
    pallet is processed (with the new location in the pallet record), all
    the pallet boxes that were originally on the pallet will be treated as a
    move to the new location.


Move a Pallet Scenaro
    The user will choose the old location.  The system will prepopulate the
    pallet boxes with all the boxes at the old location.  The user will then
    designate the new location and the system will move the boxes indicated
    by the box pallet records accordingly.


Developer Suggestions
---------------------

Perhaps a way of minimizing the amount of scanning by the user would be
to either prepopulate the pallet boxes when a location with boxes is
selected, or to have a button for the user to select to have the system
prepopulate the pallet boxes on demand.

Another suggestion is that when a QR code is scanned for a box that is
filled, to populate the pallet box with all the information from the box
record.


Pallet Management API's
-----------------------

The call for processing a pallet of boxes is:

BoxManagementClass.pallet_finish
    If pallet status is "Fill", this API will add the pallet of filled boxes
    to the specified location in the warehouse.

    If pallet status is "Merge" it will merge two or more pallets and put
    the resulting pallet boxes at the specified location.

    If the pallet status is "Move" it will move a pallet of filled boxes to
    a different location.

Note - at this time, there is no option to consume a whole pallet of filled
boxes.


Pallet Management API Details
-----------------------------

The expected input, actions, and output of the box management API calls are
shown below.

BoxManagementClass.pallet_finish
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Process a pallet of boxes and do the appropriate action to each box.

Expected Input
""""""""""""""

The pallet record with an appropriate pallet status in it.  The pallet
status will indicate if this is an addition of product to inventory
("FILL"), a move of a pallet of boxes from one location to another ("MOVE"),
or a consolidation of boxes from various old locations to a new location
("MERGE").  The associated PalletBox records will have the product and
expiration information, as well as an individual status that will guide this
processing.

Actions
"""""""

This API will walk through the PalletBox records associated with this
Pallet.  Each corresponding box will be modified as needed.

If the pallet box status is:

NEW:
    The existing box record is expected to be empty and is being
    filled with the information from the pallet box and pallet.  The
    pallet box will be added to the system.

    If the information from the ballet box and pallet record matches the
    box record already in inventory, there will be no change to the
    database.

    If the product and expiration information is the same but the location
    is different, this action will be treated as a move.

ORIGINAL:
    The box information should have been copied into the pallet
    box record because other boxes are being added to the
    pallet at this location or that this entire pallet is being
    moved to a new location.  If the only difference is the location, it
    will be treated as a move.

    If the information from the ballet box and pallet record matches the
    box record already in inventory, there will be no change to the
    database.

MERGE:
    This record will be treated the same way as if its status was "ORIGINAL".

Output
""""""

Nothing will be returned.


*******************
Activity Management
*******************


Box Activity API
================

The Box Activity API (`BoxActivityClass`_) records information in the
Activity table so that what is available can be readily discerned and that
the flow of product through the facility can be determined.

Although it has three public methods, none of them should be called directly
because the box management API's will take care of calling the appropriate
box activity API.


Box Activity API Details
------------------------

The details for each Box Management API call are documented in the source
code of the call.

_`BoxManagementClass` see BoxManagementClass in
fpiweb/support/BoxManagement.py.

_`BoxActivityClass` see BoxActivityClass in
fpiweb/support/BoxActivity.py.
