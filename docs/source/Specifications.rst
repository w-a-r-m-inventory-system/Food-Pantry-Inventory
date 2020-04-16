**************
Specifications
**************
This application will track the product managed by a food pantry.

Goals
=====

The key objectives of this system are:

#.  Track all product (food, personal care, etc.) destined to be given to
    clients.

    -   Record product coming into the warehouse supporting the pantry -
        what it is, where it is located, quantity, and expiration date.

    -   Record any movement of product in the warehouse so staff know
        where the product is at all times.

    -   Record when product is consumed or used up.

#.  Provide staff with information about the product in and flowing through
    the system.  Key points:

    -   How much of each product is in the warehouse?

    -   Where is product that is about to expire located?

    -   How much of each product has been consumed over various periods of
        time?

    -   Is there insufficient product to meet expected demand?  If so, how
        much is needed?

    -   Is there too much of a given product?  If so, how much will expire
        before it can be used?

#.  Provide a means of tracking the product that is easy to use --
    expecially by inexperienced people.

    -   Most of the people handling the product are volunteers who are
        helping for only an hour or two at a time.

    -   Ideally parts of this system can accommodate teenagers or people with
        disabilities.

Initial Approach
================

This application will initially take this approach to track the product.

Product Management
------------------

-   Product will be stored in boxes that are uniformly sized (with some
    exceptions).

-   The boxes will have three labels on the end.

    -   The first label will be a printed QR code that has a URL that
        includes a unique box number.  The URL will be such that scanning it
        will access the system to bring up a web page.  That web page will
        allow the user to check the box in, move the box to a new location,
        or check the box out of the system.

    -   The second label will identify the category of procduct contained in
        the box.  The granularity of the category will be determined by the
        distribution manager.

    -   The third label will identify the expiration date of the product
        contained in the box.  At least the year will always be identified.
        At the discretion of the distribution manager, additional labels may
        be attached that identify the half-year, quarter, or month of
        expiration.

-   The location of a box will be in a fixed place in the warehouse.  The
    distribution manager will designate the available location categories.
    Currently, locations are identified by:

    -   Row (01 - 04)

    -   Bin (01 - 09)

    -   Tier

        -   Ground level - A1, A2

        -   First level (above ground level) - B1, B2

        -   Second level (above first level) - C1, C2

    -   Boxes locations will have all three identifiers.  For example: row
        1, bin 4, tier A2.  The short form is 01-04-A2.

-   Boxes will be stored (presumably) full of product at one of the locations
    designated above.  If a box is moved, an entry in the system is required
    so it will know where the box is.

-   If a box is consumed (taken out of inventory in preparation for giving
    the contents to clients), the system will create a record with the
    following information:

    -   Box number/id
    -   Product category name
    -   Date the box was filled
    -   Expiration information
    -   Date box was emptied
    -   Location of the box when it was emptied
    -   Number of days the box was in inventory

-   The URL in the QR label will be such that scanning it will access the
    system to bring up a web page.  That web page will allow the user to
    check the box in, move the box to a new location, or check the box out
    of the system.

-   Although the boxes are usually collected and stored on a pallet, the
    system will track by box.

Web Site
========

Django will be used to present a web site that accepts the URL encoded in a
QR code.

The web site brought up by the QR code will have the following functions:

-   Identify and validate the user.

-   Checkin Product

    -   Checkin will allow the user to designate that the box of product is
        being checked in, the contents (product), location to be stored, and
        expiration date given.

-   Checkout Product

    -   Checkout will allow the box of product to be consumed (checked out)
        of inventory.

-   Move Box of Product to a new location.

-   Logout the user.

Backend
=======

A separate directory in the project will hold the backend code.

API's
-----

The backend will present the following APIs for the use of the web site:

Initial Scan
++++++++++++

This API will accept the box number from the initial QR oode scan.  It will
query the database to determine:

    -   The box exists and is empty.  If so, send back information so the
        contents, etc. of the box can be recorded.   If the box number does
        not exist, create a record for it and send back the same information.

    -   The box exists and it is full.  Send back the contents of the box and
        other information so the box can be moved or consumed.

    -   If the format of the box number is misconfigured, send back an error.



Development Configuration
=========================

Software
--------

Developers will have the following software installed and configured on their
system:

-   PyCharm (Professional or Community)
-   Python 3.6 or later
-   PostgreSQL
    -   Server 11.0 or later
    -   pgAdmin 4.0 or later

Project
-------

Each developer will have a fork of the main repository on GitHub.  A local
clone of their fork will be used on the developer's system to manage changes
to the system.

Changes will be implemented by:

#.  Branching the local repository
#.  Making changes in the branch
#.  Testing the changes in the branch
#.  Merging the changes in the branch into the local master
#.  Retest/regression test
#.  Push the changes into the developer's fork on GitHub
#.  Submit a pull request into the main repository

See the :doc:`Developer Documentation <DeveloperDocumentation>` for more
information about how to be a contributor to this project and how to get
started.


Tasks
=====

Please refer to the document :doc:`Outstanding Tasks <OutstandingTasks>` for
specific items that need to be accomplished.
