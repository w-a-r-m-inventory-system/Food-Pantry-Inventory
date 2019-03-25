:orphan:

*********************
PostgreSQL Guidelines
*********************

This document discusses how to set up PostgreSQL for use with this inventory
system.

Download
========

Download the appropriate installer for your operating system from
https://www.postgresql.org.  The installer will include both the programs
for the server and a separate GUI program for managing the server(s) desired.

In addition to having downloads for various systems, it has a link to a nice
description of what databases - PostgreSQL in particular - are all about.

Note that there are no installers for Unix/Linux systems because every
flavor has a way of installing PostgreSQL as and option or automatically
installs it as part of the OS install.

Installation
============

Install PostgreSQL as you would most programs.  There are a few points to
consider during installation.

-   The installer will create another user on your system.  The suggested
    name for that user id is "postgres".

-   The password for that user can be whatever you want it to be so choose
    something memorable and unlikely to be guessed or "brute forced" by
    someone else.

-   Be sure to note which port that PostgreSQL uses for the server.  The
    default is 5432 but that is not mandatory.

-   It will install the data files somewhere.  It does not matter for the
    purposes of this program just where they are installed so long as they
    are not in your way.  Perhaps a separate directory could be created
    somewhere and the files installed there so they don't get commingled
    with files for something else.

-   In addition to the server software, the installer will install a program
    called pgAdmin 4.  This program will let you administer your server so
    you will need to run it on occasion.

-   If the installer presents a window with the installation details, copy
    that information to a text file somewhere for later reference.

Configuration
=============

After the installer is done, start the pgAdmin 4 program.  It will cause a
page to be displayed in your browser and go away.  What actually happened is
that it started a second server just for pgAdmin 4 (like Django does for our
application) and lets you interact with it through the browser.

Once the pgAdmin 4 web page is displayed, open LocalGrp and LocallyServedDB
under that.  Create a new (empty) database called "WARM".

-   The application will take care of creating the tables and filling them
    with data.

-   pgAdmin 4 is the tool you will use to look at (and possibly modify) the
    data from the application so you may want to wander around in pgAdmin 4
    and get comfortable with it.
