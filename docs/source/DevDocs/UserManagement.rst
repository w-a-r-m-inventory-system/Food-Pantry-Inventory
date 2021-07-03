###############
User Management
###############

*******
Summary
*******

Users allowed access to the system are divided into three groups: Volunteer,
Staff, and Administrator.  The three

    ===================  =========
    Group Identifier(1)  Access
    ===================  =========
    Volunteer            `Volunteer User Access`_
    Staff                `Staff User Access`_
    Admin                `Administrator User Access`_
    ===================  =========

1.  This is the value in the auth_group table.

Volunteer User Access
=====================

Volunteers have the most limited access.  They are allowed the following
functions:

-   Login to the system
-   Add boxes
-   Checkin/checkout boxes and pallets
-   Move boxes and pallets
-   Check box status
-   change their own password
-   change their name, email address, title (but not their userid)
-   view product examples

Staff User Access
=================

Staff access can do the following:

-   Can manage all user data:

    -   boxes
    -   durable data (e.g. product, box type, location, etc.)
    -   constraints

-   Can print QR labels
-   Can dump activity data
-   Can add user information:

    -   Add a new userid, name, title,  permisison level (staff or
        volunteer) and initial password

-   Can change user information:

    -   permission level (volunteer -> staff, staff -> volunteer).
    -   Can force user to have a different (temporary) password.

        -   The user must use the temporary password the first time and
            change it to something else immediately.

    -   Can block a staff or volunteer user’s access (inactivate a user).
-   Can use the Django admin web site -- except for accessing the user
    and group tables.
-   Everything that a volunteer can do


Administrator User Access
=========================

Admin access has full access to all menu picks - including all
Django admin pages.

An administrator can:

-   Add or block another administrator
-   Add or block any other user
-   Everything a staff member can do

***********************
User Management Screens
***********************

This section documents each user screen and provides details not given
elsewhere.

Login Screen
============

This is a simple login screen that requests a user id and password.  It will
be accessible for all users.  This screen will also be the first screen
presented to the user when the main (default) URL is given in the user's
browser.

-   The userid and password are kept in the default Django table
    (django_user).

-   This userid must have several associated records.

    -   A fpiweb_profile record to hold application-specific data.
    -   At least one auth_user_groups record to identify what level of
        permissions are permitted for this userid.

-   If the fpiweb_profile record indicates that the user must change their
    password, this screen will provide a place to do so.

-   A user must be an "active" user.

Users who fail to provide a valid login and pasword, who fail to provide a
valid new password when requested to do so, or whose credentials fails to
meet the above criteria will be notified with a message "Invalid
credentials, please try again".  No more detail will be provided on the login
screen.  After three tries, for a userid that is valid, the userid will be
set to inactive and must be changed by another qualified user before this
userid can be used again.

Additional options:

-   Include a check box to allow the user to change their password as
    desired (after being validated).
-   Forbid changing passwords more often than once a day (future).
-   Do not require a user to change thier password (except if forced by a
    staff or administrator.

Passwords
---------

Passwords must meet the following criteria:

-   Must be at least eight (8) characters long
-   If less than twelve (12) characters long, must contain a mix of at
    least three of these classes:

    -   upper case letters
    -   lower case letters
    -   numbers
    -   special characters

-   Can be up to at least 128 characters long.

    -   The entire password will be hashed, not just the first eight
        characters

There may be other constraints added later as needed for security protection.

Logout Screen
=============

This screen is accessible by all users.  When chosen, it will invalidate any
cookies, csrf token, etc. so that the user must login again before resuming
operations.

This screen will have a link to the login screen.

System User Maintenance Screen
==============================

Only staff or administrators are permitted to use this screen.
Screen will:

-   Show (scrolling) list of userids and associated info:

    -   fields shown in scrolling list
        -   userid
        -   first and last name
        -   permission level
        -   active flag
    -   Administrator level permissions will see all users
    -   Staff level permissons will see only staff and volunteers

-   Selecting a user will show all the current details about that user.

-   Button available to add a new user.

Fields Displayed (see Legend_ and `Table Notes`_ for additional explanation)

    =================  ========  ===========
    Field              New User  Change User
    =================  ========  ===========
    userid             CM[1]     U
    first name         CM        C
    last name          CM        C
    title              C[2]      C(2]
    email address      CN        CN
    permission level   SM[4]     S[4]
    active             BM        CB
    password           CME[3]    CE[3]
    =================  ========  ===========

_`Legend`

    =========  =======
    Indicator  Meaning
    =========  =======
    M          Mandatory
    C          Changeable
    U          Unchangeable
    N          Not required (blank allowed)
    E          Encrypted
    S          Selection of: Administrator(4), Staff, or Voluneer
    B          Boolean: Yes or No selection
    =========  =======

_`Table Notes`

.. [1]  Userid must be unique and are encouraged to be at least 6 characters
        long.

.. [2]  Title will default to "Volunteer", "Staff", or "Administrator"
        depending on the permission level given.

.. [3]  If set or changed, the password will never be visible at any time, and
        must be entered twice.

.. [4]  Only administrators can set the permission level of a user to
        administrator.
