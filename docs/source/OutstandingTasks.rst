*****************
Outstanding Tasks
*****************

There are numerous tasks and activities that remain to be accomplished by
someone before this project will be complete.  They have been divided into
the following milestones.

Milestone Descriptions
======================

_`M-V0.95`  Version 0.95 - Complete functionality

_`M-V1.0`  Version 1.0 - Minimum Viable Product (MVP)

_`M-V1.1`  Version 1.1 - First polish

_`M-ReWk`  Needs to be reworked.


Task Tables by Milestone
========================

..  table::  Milestone 0.95 Tasks - Complete Functionality
    :widths: auto
    :align: left

    ========  ==========  ====================================================
    Issue #   Milestone   Title
    ========  ==========  ====================================================
    `I-216`_  `M-V0.95`_  Get formal permission to use WARM logo
    `I-215`_  `M-V0.95`_  Determine source for X509 certificates
    `I-213`_  `M-V0.95`_  Ensure system can be used from a smart phone/tablet
    `I-212`_  `M-V0.95`_  Cloud VM
    `I-210`_  `M-V0.95`_  Admin Permissions
    `I-209`_  `M-V0.95`_  Staff Permissions - can:
    `I-208`_  `M-V0.95`_  Volunteer Permissions - can:
    `I-207`_  `M-V0.95`_  Implement permission levels though out the app
    `I-205`_  `M-V0.95`_  Setup a docker container for Nginx
    `I-204`_  `M-V0.95`_  Setup a docker container for Django and uWSGI
    `I-203`_  `M-V0.95`_  Setup docker container with PostgreSQL configuration
    `I-202`_  `M-V0.95`_  Implement Manual Pallet Management
    `I-178`_  `M-V0.95`_  Manual box checkin needs to be streamlined
    `I-173`_  `M-V0.95`_  Build Pallet needs to set pallet status
    `I-167`_  `M-V0.95`_  Results of Mike R.'s original testing
    `I-161`_  `M-V0.95`_  Move Pallet
    `I-115`_  `M-V0.95`_  Rework the API of theQR label print program
    `I-88`_   `M-V0.95`_  Make a docker image of project to run locally
    ========  ==========  ====================================================

..  table::  Milestone 1.0 MVP Tasks
    :widths: auto
    :align: left

    ========  ==========  ====================================================
    Issue #   Milestone   Title
    ========  ==========  ====================================================
    `I-222`_  `M-V1.0`_   Let’s Encrypt X509 certificate
    `I-221`_  `M-V1.0`_   Setup production with “dummy” data initially
    `I-220`_  `M-V1.0`_   Test production for security
    `I-219`_  `M-V1.0`_   Test backup
    `I-218`_  `M-V1.0`_   Arrange backup of data and schema in database.
    `I-217`_  `M-V1.0`_   Script production fallback
    `I-214`_  `M-V1.0`_   Script production (docker, VM, cloud provider)...
    `I-206`_  `M-V1.0`_   View/search the Product Examples table
    `I-190`_  `M-V1.0`_   Build Pallet: set pallet ID in profile
    `I-176`_  `M-V1.0`_   Change user password
    `I-175`_  `M-V1.0`_   Add/Change/Delete a User
    `I-145`_  `M-V1.0`_   Document clearing start/end exp. mo in Build Pallet
    ========  ==========  ====================================================

..  table::  Milestone 1.1 First Polish Tasks
    :widths: auto
    :align: left

    ========  ==========  ====================================================
    Issue #   Milestone   Title
    ========  ==========  ====================================================
    `I-227`_  `M-V1.1`_   Checkout a pallet of boxes (future)
    `I-226`_  `M-V1.1`_   Generate Location Table from Row, Bin, and Tier
    `I-225`_  `M-V1.1`_   Reorganize menu picks by most frequently used
    `I-224`_  `M-V1.1`_   Location Table - build ACID screens
    `I-223`_  `M-V1.1`_   Change a box’s quantity and box type
    `I-211`_  `M-V1.1`_   Eliminate the standalone QR print program
    `I-198`_  `M-V1.1`_   Build Pallet Screen UI Change w/ no previous pallets
    `I-192`_  `M-V1.1`_   Build Pallet Screen. Save more in Pallet Box record
    `I-189`_  `M-V1.1`_   Ensure that the "Evans" box type is default
    `I-174`_  `M-V1.1`_   Delete a pallet
    `I-138`_  `M-V1.1`_   Enhance README.md with a more detailed purpose.
    `I-89`_   `M-V1.1`_   Improve README.md etc. for new developers
    `I-54`_   `M-V1.1`_   Product Examples Table - Build ACID screens
    `I-42`_   `M-V1.1`_   Box Type Table - Build ACID screens
    `I-41`_   `M-V1.1`_   Product Table - build ACID screens
    `I-40`_   `M-V1.1`_   Product Category Table - build ACID screens
    ========  ==========  ====================================================

Task Descriptions by Issue
==========================

These task provide details for all the known activities that remain to be
done. Each is identified with an issue number as labeled in Github.  As tasks
are completed the details will be moved to an appropriate location elsewhere
in this documentation.

_`I-227`  Checkout a pallet of boxes (future)
---------------------------------------------

On rare occasions, the food pantry will give a whole pallet of product to
another food pantry.  It would be convenient to add this functionality to
the system -- eventually.

_`I-226`  Generate Location Table from Row, Bin, and Tier
------------------------------------------------------------------------------

Factor in exclusions given in the Constraints table

_`I-225`  Reorganize menu picks by most frequently used
------------------------------------------------------------------------------

-   Perhaps this can be done when first going to production.

    -   If so, it may need to be reviewed again after the clients gain
        experience with the system.

_`I-224`  Location Table - build ACID screens
------------------------------------------------------------------------------

Add editing for the Location Table - somewhat similar to the Constraints Table.

-   Perhaps a new entry could be "built up" by choosing a combination of valid
    row, bin, and tier.
-   Changing or deleting an entry should be forbidden if any currently filled
    box or pallet refers to it.

-   Currently this functionality is available with the Django admin subsite.

_`I-223`  Change a box’s quantity and box type
------------------------------------------------------------------------------

Provide a way for staff to change a box’s quantity and box  type.

-   A particular box can have a quantity not equal to the quantity in the
    box type
-   Verify that no other code changes the box quantity once set
-   Initial quantity set from box type when box is added to inventory

    -   All ways of adding a box to inventory should use BoxManagement rather
        than setting the box type and quantity directly.

_`I-222`  Let’s Encrypt X509 certificate
------------------------------------------------------------------------------

Identify and document how to obtain and automatically renew a Let’s Encrypt
X509 certificate

_`I-221`  Setup production with “dummy” data initially
------------------------------------------------------------------------------

This is so staff and volunteers can gain experience with the system

_`I-220`  Test production for security
------------------------------------------------------------------------------

Brian Caslow offered to do this.

The system should be tested for vulnerabilities at least quarterly.

_`I-219`  Test backup
------------------------------------------------------------------------------

-   Restore data from backup to ensure the the backup is valid
-   Schedule the tests at least quarterly

_`I-218`  Arrange backup of data and schema in database.
------------------------------------------------------------------------------

-   Backup data and schema only to minimize the size of backup
-   Transfer backup out of cloud to other storage securely
-   Determine frequency of backup to minimize data loss
-   Test!

_`I-217`  Script production fallback
------------------------------------------------------------------------------

So system can be quickly reverted to the previous version if needed

-   test!

_`I-216`  Get formal permission to use WARM logo
------------------------------------------------------------------------------

Get formal permission to use the WARM logo for the web site and the
documentation

_`I-215`  Determine source for X509 certificates
------------------------------------------------------------------------------

Determine if we need to set up X509 certificates from Let’s Encrypt or if
WARM already has certificate we will be allowed to use.

This issue may depend on issue #222.

_`I-214`  Script production (docker, VM, cloud provider)...
------------------------------------------------------------------------------

This issue depends on issues #203, #204, and #205 to be completed.

Also depends on issue #215.

_`I-213`  Ensure system can be used from a smart phone/tablet
------------------------------------------------------------------------------

Test using both Android and iOS devices, both smart phones and well as
tablets of each kind.

-   Verify that a camera can be used to scan a QR code at the appropriate
    place.
-   Optionally test with other devices, such as a Fire, etc.

_`I-212`  Cloud VM
------------------------------------------------------------------------------

-   Identify cloud provider we will use for production
-   Identify costs, who will pay for it and how it will be billed

_`I-211`  Eliminate the standalone QR print program
------------------------------------------------------------------------------

Reason - it needs access to the database to skip box numbers already in
use.  However, when the live database is in production, providing secure
access to the database will be more difficult than just using the menu pick.

_`I-210`  Admin Permissions
------------------------------------------------------------------------------

Has full access to all menu picks - including the Django admin pages

_`I-209`  Staff Permissions - can:
------------------------------------------------------------------------------

- Can manage all user data:

    - boxes
    - durable data (e.g. product, box type, location, etc.)
    - constraints

- Can print QR labels
- Can dump activity data
- Can add user information - including permission level and initial password
- Can change user permission level (volunteer -> staff, staff -> volunteer)
- Can block a user’s access
- Everything that a volunteer can do

_`I-208`  Volunteer Permissions - can:
------------------------------------------------------------------------------

- Add boxes
- Checkin/checkout boxes and pallets
- Move boxes and pallets
- Check box status
- change their own password
- change their name, email address, title
- view product examples

_`I-207`  Implement permission levels though out the app
------------------------------------------------------------------------------

-   Only login page does not require the LoginMixIn.
-   Each page will verify if the user is allowed to access that page.
-   Throws a polite error message and allow return to previous page if not.
-   So far, only the Add user page and the change user permission page will
    have conditional logic based on the permission of the user.
-   Perhaps this can be isolated to one class or function that contains the
    necessary logic.

_`I-206`  View/search the Product Examples table
------------------------------------------------------------------------------

-   This view/search should be a “full text” search of the Product Examples
    Table.  E.g. a search for “peas” should show all records that have peas
    somewhere in the description including black eyed peas, green peas,
    young peas and peasant (if exists).
-   Each entry found should list the product that is appropriate for it so
    that the user can select the proper product.
-   This is particularly important for product examples that could be in in
    more than one product.

    -   Beef stew could be in either meat or soup.
    -   It is up to the food pantry to decide.

-   This view search should be available to any logged in user.

This view or search should be available whenever a product is being
selected.  How to accomplish this is up to the implementor.

_`I-205`  Setup a docker container for Nginx
------------------------------------------------------------------------------

- Build container with a fresh copy of a specified version of Ngnix
- Uses a “secret” configuration including:

  - Specified IP and port to allow web traffic (possibly non-standard)
  - Specified IP and port to send web traffic to the Django container
    (possibly non-standard)

- Includes X509 certificates to enable HTTPS - possibly from Let’s Encrypt
- Includes any hardening needed for production

_`I-204`  Setup a docker container for Django and uWSGI
------------------------------------------------------------------------------

-   Builds container with a fresh copy of a specified version of Django
-   Loads other production dependencies and libraries
-   Uses a “secret” configuration including:

    -   Database user id and password
    -   Specified IP and port to access database (possibly non-standard)
    -   Specified IP and port to receive web traffic (possibly non-standard)

-   Includes uWSGI installation and configuration
-   Includes any hardening needed for production

_`I-203`  Setup docker container with PostgreSQL configuration
------------------------------------------------------------------------------

-   Builds container with fresh copy of a specified version of PostgreSQL
-   Uses a “secret” superuser id and password and other configuration parameters
-   Loads the schema from a specified source
-   Loads data from a specified backup source
-   Allows access from a specified IP and port (possibly non-standard)
-   Includes automatic backup of the database at a specified interval
-   Includes means of exporting the backup securely
-   Includes any hardening needed for production

_`I-202`  Implement Manual Pallet Management
------------------------------------------------------------------------------

Implement the remaining Manual Pallet Management screens.

- Start a new pallet

  - Request a pallet name
  - Verify that the new pallet name is different from any other pallet name

    - If match, show error message and allow different entry

  - Proceed to common screen described below
  - Allow user to return to menu if desired

- Select a pallet in progress

  - Show a list of existing pallet names and allow selection of one of them
  - Proceed to common screen described below
  - Allow user to return to menu if desired

Common screen
- Present a screen somewhat similar to the second Build Pallet screen.
- Request a box number (text only, no QR code)

  - Display error if box not in system or is full — allow reentry

    - (Different from Build Pallet - may be keying error)

- Show box number
- Request product, expiration year (and optional start/end months)
- Allow box to be removed from the pallet
- Allow box information to be changed
- Provide menu pick to complete the pallet.

Internal requirements:

-   Set or replace Pallet ID in Profile Record as soon as pallet is created
    or selected.
-   Add or update Pallet Box Records as soon as user moves on to the next box.

Validate product and expiration date information

- Delete Pallet Box Record immediately if user deletes it from list
- Verify that a golem box number is not specified twice

  - Check can be delayed until ready to complete the pallet

_`I-198`  Build Pallet Screen UI Change w/ no previous pallets
------------------------------------------------------------------------------

On the Build Pallet screen, an improvement would be that when there are no
Pallet records, only the Add Pallet input area would be shown. In that case
the Select Pallet input area would be hidden.

_`I-192`  Build Pallet Screen. Save more in Pallet Box record
------------------------------------------------------------------------------

Comments from existing issue:

Here's the scenario as Travis describes it:

I added a few boxes to a pallet using the main build pallet screens, then
went back to the manual pallet menu to see how it displayed. I discovered
that the main build pallet screen was adding the box to the pallet box
records, but was not filling in the product or expiration date until the
pallet complete is selected. This can be a problem because if one person
starts a pallet, then leaves, another person cannot pick up where the first
person left off

This behavior isn't surprising. When the box is scanned the product and
expiration dates are unknown. If the user fills in product and expiration
date and clicks the "Pallet complete" the product and expiration date
information is saved in the database. To allow a user to partially complete
a pallet and then leave it and pick it up later we need an additional
mechanism. One thought would be to have a save button, but the user has to
remember to click it. I'm thinking of adding an on-change event handler
that would update the record in the database whenever a field changes.

Scenario and comments from Travis' original email:

I added a few boxes to a pallet using the main build pallet screens, then
went back to the manual pallet menu to see how it displayed. I discovered
that the main build pallet screen was adding the box to the pallet box
records, but was not filling in the product or expiration date until the
pallet complete is selected. This can be a problem because if one person
starts a pallet, then leaves, another person cannot pick up where the first
person left off. I second concern is that two people cannot work together
to check in all the boxes on a new pallet. A third concern is that a person
cannot switch back and forth between two pallets while they are filling up.

Is this a limitation that we need to document? Please share your thoughts
about this.

If an on-change event handler or a save button is appropriate to save the
data to the pallet_box record, then so be it.

If it would be simpler, perhaps the "Scan a Box" button and the two links
"Select another pallet" and "Return to main page" could be overloaded to
save any previous box data? Would that be easier?

Ideally the solution would include functionality to:

-   Allows someone to stop working on a pallet and resume work later.
-   Allows someone else to resume work on a pallet started by someone else.
-   Allows multiple people to work on separate pallets.
-   Allows multiple people to work on the same pallet.

However, current functionality is sufficient for initial production.

_`I-190`  Build Pallet: set pallet ID in profile
------------------------------------------------------------------------------

Currently, Build Pallet creates a pallet record with a new pallet is chosen.
It needs to also set the profile for this user to point to the pallet
record just created.

If a pallet is selected in the first Build Pallet screen, the profile
record needs to be updated immediately.

The reason this is needed is that various pages display the information
about the active pallet -- and sometimes the boxes associated with the pallet.

_`I-189`  Ensure that the "Evans" box type is default
------------------------------------------------------------------------------

Ensure that any time a box is added to inventory (new box number, not just
filled) that the "Evans" box type is at the top of the list. This will be
the default box type for any new boxes.

Perhaps the default box type should be an entry in the constraints table so
it is not hard-coded to the WARM food pantry.

The documentation should how to set this default.

-   Perhaps as a default indicator so that it can be first regardless of sort
    order
-   An alternate possibility would be to add a “sort order” field so all the
    box types can be shown from most frequently used to least frequent

_`I-178`  Manual box checkin needs to be streamlined
------------------------------------------------------------------------------

Currently manual box checkin asks for box number, contents, etc. in
separate screens. it needs to be changed so all the needed information if
filled in on one screen.

-   Add ability to specify start/end expiration months.

_`I-176`  Change user password
------------------------------------------------------------------------------

Provide a way for any active user to change their password.
Passwords must meet certain minimum requirements:

-   Must be at least 8 characters in length
-   Must have at least one alphanumeric character.
-   If length is less than 12 characters, must have:
-   A upper case character
-   A lower case character
-   A number
-   Cannot contain any form of these words:
-   WARM, password, 1234, the current month in letters or numbers

The screen must require both the valid old password and require the new
password be typed in twice.

The screen should provide help about what a minimum password requires,
except that it should only say that certain words are forbidden.

Access to this screen should require that the user login first.

-   Perhaps use a library (like password-checker) to prevent short and easy to
    guess passwords and password permutations (e.g. changing the suffix to
    the next month name or number)

-   If easy to do, provide a password expiration after some number of days
    (set in Constraints) but do not implement it for now.

_`I-175`  Add/Change/Delete a User
------------------------------------------------------------------------------
Need code to add a user to the system.

-   Must supply values for these fields:
-   Assigned userid
-   First and Last names
-   Email address (optional)
-   Initial password
-   Title
-   Role (group permission)

Need code to change a user

-   Update all but the password

Need code to delete a user

-   Change Active flag to effectively stop a user from accessing the system.

Add requires an initial password which user is required to change on first
login

-   Permitted roles (Permission levels)
-   Staff can set staff or volunteer
-   Admin can set any level

_`I-174`  Delete a pallet
------------------------------------------------------------------------------
-   Current workaround, complete the pallet with no boxes
-   Possibly limited to staff

Provide a way to remove a pallet.

-   Perhaps it is adequate to do this from the Admin menu.
-   Ensure that all pallet_box records are also deleted -- but without
    deleting the associated box records.
-   Require that this can be done only by Staff level permissions or above.
-   Document how to do this.
-   If separate code, it can wait until after the first release.

If done via Admin, test it before going live.

_`I-173`  Build Pallet needs to set pallet status
------------------------------------------------------------------------------

The Build Pallet screen and supporting code needs to set the pallet status
to Pallet.FILL by the time the finish pallet action is taken.

-   There is temporary code in BoxManagement.pallet_finish which needs to
    be removed after the above fix is in place.

-   Probably a test needs to be added to verify that the pallet status is
    always set.

_`I-167`  Results of Mike R.'s original testing
------------------------------------------------------------------------------

Attached is the results of Mike's initial testing. When you address any of
these issues, please create a separate issue for it so it can be assigned
to you.
QWebPageCheck.pdf

Attached is a spreadsheet equivalent of the PDF attached above.
QWebPageCheck.xlsx

_`I-161`  Move Pallet
------------------------------------------------------------------------------

1.  Enter "Move from" location using row, bin, and tier <select> elements.
    Upon submit display form with errors if the location doesn't exist
    or there are no boxes at that location.

#.  If the "Move from" location exists and has boxes display row, bin,
    and tier <select> elements to select the "Move to" Location. This
    page will also list the boxes at the "Move from" location. Upon
    submit display form with errors if the "Move to" location doesn't
    exist

#.  If there are boxes at the "Move to" location let the user know that
    and give them an option go back and select another location or
    continue. (continuing is merging pallets and that's ok)

#.  Generic "N boxes moved from A to B" message.

#.  Use BoxManagementClass.pallet_finish to update the database.

    Verify that the code sets appropriate pallet status before passing
    pallet to BoxManagement

_`I-145`  Document clearing start/end exp. mo in Build Pallet
------------------------------------------------------------------------------

When using a QR code to scan a box, the product and expiration date will
default to whatever the previous box contained -- including the beginning
and ending months. That is valid behavior. The product and expiration date
can be adjusted as needed. However, if the previous box had a non-zero
start and end month, the start and end month for this box cannot be set
back to zero.

Although the month start and end cannot be set to zero, they can be blanked
out (via backspace). Thus this is now just an issue that needs to be
documented and closed.

- Alternately allow the start and end months to be reset to zero to clear

_`I-138`  Enhance README.md with a more detailed purpose.
------------------------------------------------------------------------------
Add more comments about what the project does, how it plans to accomplish
it, sample screen shots, etc. The goal is to provide a first-time visitor
with a what they can expect to accomplish with this project.

Perhaps comments about how it could be extended to be used for other food
pantries would be helpful.

_`I-115`  Rework the API of theQR label print program
------------------------------------------------------------------------------

The current version of the QR label print program does not provide an easy API to be used by a web-based call or a GUI standalone program. It needs to be reworked so that a simple call can be made to get back the SVG XML. Perhaps it should also be able to provide a png on request.

Rather than implement the QR printing program as an API to the standalone program, this functionality will be moved to the online code.  The reasons are given in issue #71.

Requirements:
- Produce full pages of PDF formatted document to download and subsequently print.
- if direct access to the printer is easy to implement, allow that as an option.
- Ask for starting box number and count of labels desired

  - Skip any box numbers that are already in the system.

- Ask if boxes are to be created in the system

  - If so, ask for the default box type.

- Optionally ask for a prefix to the box number

  - May need to prefix the box number with a URL for access to production

- Format box number with a mandatory "BOX" (in caps)
- Format the box number as a five digit number with leading zeros as needed.
- Assume:

  -   letter size paper

      -   portrait orientation

  -   1/2 inch outer margin on all sides
  -   3 labels across
  -   4 labels down
  -   each label has 1/4 in margin on all sides
  -   print in ascending order, left to right, top to bottom
  -   leave unused label location completely blank
  -   format pdf to print whole pages with no blank pages at the end

_`I-89`   Improve README.md etc. for new developers
------------------------------------------------------------------------------

Revise the developer documentation from README.md on back to reflect
current practices and procedures.

Improve the flow to the startup documentation so it is either all in
the README.md or linked directly so that someone does not need to visit the
wiki and then dig in the docs to find out how to set up their copy of the
project.

_`I-88`   Make a docker image of project to run locally
------------------------------------------------------------------------------

A Dockerfile needs to be  made to build an image of the Inventory system
so that it can be ran locally in a container. This ultimately might be
expanded later to having the app and its components in containers.

One of the requirements of the docker image  is a web server such as a
Apache web server. This may mean one Docker container or perhaps up to
three are needed.

-   Database
-   Application (Django)
-   Web Server (e. g. Apache or equivalent)

This is to be decided after someone researches how best to configure Docker.

-   Includes defining the docker containers and loading configurations,
    code and data
-   Separate docker containers and configuration for PostgreSQL, Nginx,
    and Django with uWSGI.

Notes:

-   Nginx was selected as the web server
-   uWSGI was selected as the production Django interface to the web server

See also these issues:

-   Issue #203 For configuring Docker for PostgreSQL
-   Issue #204 For configuring Docker for Django and uWSGI
-   Issue #205 For configuring Docker for Nginx

_`I-54`   Product Examples Table - Build ACID screens
------------------------------------------------------------------------------

Recently we added a new table - product_examples. We need screens to
list/add/change/delete the entries in this table. Each entry is associated
with exactly one product.

More documentation about this table will be added in the next few days.

Build web pages that will allow an authorized user (i.e. staff or admin) to add, change and delete
product example entries.

-   Each product example entry must be associated with one (and only one)
    product.
-   Changing a product example entry may include changing which product is
    associated with it.
-   Currently only the roles staff or admin may access this set of screens.

See also issue #206 for how this table will be used.

_`I-42`   Box Type Table - Build ACID screens
------------------------------------------------------------------------------

Build screens to list, add, change, and delete box types.

-   Include requirement that the user must be logged in before these screens
    can be used.
-   Add link to index page to get to the list screen.

Build web pages that will allow an authorized user to add, change and
delete box type entries.

-   Deleting a box type will not be permitted if there are any box entries
    referencing this box type.

This could be done using the admin screens. Create a BoxTypeAdmin class and
register it in fpiweb/admin.py. There are a couple examples in the 
admin.py or you can check the documentation here. In addition
to list_display you might want to consider other ModelAdmin options. The
Django permission system provides a lot of granularity to control who can
do what.

_`I-41`   Product Table - build ACID screens
------------------------------------------------------------------------------

Build screens to list, add, change, and delete products.

-   Include requirement that the user must be logged in to use these screens.
-   Add link to index page to get to the list screen.

Build web pages that will allow an authorized user to add, change and
delete product entries.

-   Each product entry must be associated with one (and only one) product
    category.
-   Changing a product entry may include changing which which product category
    is associated with it.
-   Deleting a product entry will be permitted only if it has no associated
    product example entries.

Currently handled by the Admin menus.

_`I-40`   Product Category Table - build ACID screens
------------------------------------------------------------------------------
Need screens to list, add, change, and delete product categories.

-   Include requirement that the user must be logged in to use these screens.
-   Include link on index page to get to the list screen.

This functionality is currently provided by the Admin menus.
