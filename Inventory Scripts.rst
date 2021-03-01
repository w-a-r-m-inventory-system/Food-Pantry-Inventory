##############################################################################
inventory Scripts - Explanation
##############################################################################

This document provides information about the inventory scripts included in
this project.

******************************************************************************
Purpose
******************************************************************************

The inventory scripts were created to minimize the amount of typing needed
to start, stop, review, and otherwise manage the docker containers used here.

Controlling Script
==============================================================================

The script **inv.project-constants-sample** contains all the variables used in
the various inventory shell scripts.  It is a sample.  To use it for
production, copy it to **inv.project-constants.prod** and modify it as
needed.

Note that it is deliberately not marked as executable
as a reminder that this script must be **sourced** rather than executed.

Start and Stop Scripts
==============================================================================

=====================  =====================================================
Start Script Name      Purpose
=====================  =====================================================
inv-build.sh           Construct the docker containers from images pulled from
                       the Docker Hub
inv-run.sh             Bring "up" the three docker containers
inv-migrate.sh         Apply any database migrations needed to the db container
inv-adddata.sh         Add selected fixtures to the database
inv-collectstatic.sh   Populate the **staticfiles** container
inv-adduser.sh         Add the first superuser to the database
inv-full-up.sh         Convenience script that runs all of the above scripts
                       except the build script
=====================  =====================================================

=====================  =====================================================
Stop Script Name       Purpose
=====================  =====================================================
inv-stop.sh            Bring "down" the three docker containers
inv-clear-all.sh       Runs the above script then tries to remove all the
                       other networks, volumes, and images
=====================  =====================================================

Inspection
==============================================================================

These scripts allow for inspection of containers and volumes.

=====================  =====================================================
Script Name            Purpose
=====================  =====================================================
inv-check-config.sh    Check the docker-compose configuration file for errors
inv-view-all.sh        See a list of all containers, volumes, networks, and
                       images
inv-peekdb.sh          Access the database container with an interactive shell
inv-peeknginx.sh       Access the nginx container with an interactive shell
inv-peekweb.sh         Access the web container with an interactive shell
inv-db.sh              Access the database inside the db container with psql
inv-inspect-vols.sh    See docker information about all three volumes
=====================  =====================================================

Logs
==============================================================================

These scripts allow inspection of the various logs.

=====================  =====================================================
Script Name            Purpose
=====================  =====================================================
inv-logs-all.sh        See real-time logs from all three containers.
inv-log-db.sh          See a snapshot of the log from the database container
inv-log-nginx.sh       See a snapshot of the log from the nginx container
inv-log-web.sh         See a snapshot of the log from the web container
=====================  =====================================================

Start Browser
==============================================================================

These scripts are convenience scripts for starting a browser (probably work
only on a mac).

=====================  =====================================================
Script Name            Purpose
=====================  =====================================================
inv-tmain.sh           Opens a web browser with the main url (i.e. /)
inv-tadmin.sh          Opens a web browner on the Django admin login page
=====================  =====================================================


Notes
==============================================================================

-   The underlying purpose of writing these scripts and getting them to work
    was so that I understood how to label various parts and control
    locations of various properties and files.

-   My goal is to write a python script to manage all aspect of a project
    without any assumptions or "defaults" that I don't know how to manage.

-   Another reason for writing these scripts is that I am lazy and forgetful
    This provides reminders of how Docker works and perhaps will provide
    illumination for others.
