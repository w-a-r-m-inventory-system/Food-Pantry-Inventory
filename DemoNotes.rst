##############################################################################
Notes and Comments
##############################################################################

These are notes and comments that I made while working through the
`tutorial <https://testdriven
.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/#gunicorn>`_.
The chapter names are based on the git branches I used combined with the
section titles in the demo.

******************************************************************************
master - Project Setup
******************************************************************************

I used PyCharm to set up the project directory, virtual environment, and git.

I created a .gitignore file with the usual suspects.

I preloaded the libraries for Django, psycopg2-binary, and uWSGI into the
virtual environment that PyCharm created.

Anomaly - git would not allow me to create a branch until I had executed my
first commit.  Thus this commit includes:

-   Django directory structure and files created by startproject
-   Includes sqlite.db file used for the first test.
-   requirements.txt file with all libraries loaded into the virtual
    environment.

******************************************************************************
01-AddDjangoApp - Project Setup (continued)
******************************************************************************

Started preparing for switch to postgreSQL by deleting the sqlite database.

******************************************************************************
02-DjangoInDocker - Docker
******************************************************************************

Actions taken:

-	Deleted the sqlite.db as directed.
-   Created the Dockerfile in app as specified.
-   Created the docker-compose.yaml file in the project root.
-   Updated the settings.py file in the hello_django directory.
-   Created the .env.dev file in the project root.  Note this file name
    begins with a period.
-   Moved requirements.txt from root directory to the /app subdirectory.

When I ran the ``docker-compose build`` command, it blew up.  After looking
at this `stack overflow article <https://stackoverflow .com/questions/59215480/how-fix-my-docker-compose-error-with-psycopg2>`_
I was able to narrow down the problem.

What worked:

-   changing line 2 of the Dockerfile from ``FROM python:3.8.3-alpine`` to
    ``FROM python:3``.

What did **not** make any difference:

-   changing ``pip`` to ``pip3``
-   Adding ``sudo apt`` and ``sudo apt-get`` commands.
-   Adding thee above without the ``sudo``.
-   Removed secondary requiremens from requirements.txt.
-   Changed specific versions to "*" in requierments.txt

After the above changes, testing with docker up was successful.

******************************************************************************
03-PostgreSQLInDocker - Postgres
******************************************************************************

I added the additional info to ``docker-compose.yaml``, ``.env.dev``,
``settings.py`` and ``Dockerfile``.  The ``psycopg2-binary`` library was
already in ``requirements.txt``.

When I ran the ``docker-compose up -d --build`` command, it blew up stating
that it couldn't find the ``apk`` command.  I tried changing the
``FROM python:3`` back to ``FROM python:3.8.3-alpine`` and it blew up trying
to build the binary for uWSGI from scratch.  Perversely, it successfully
built the wheel for ``psycopg2-binary``.

Interim solution;

-   Switched back to ``FROM Python:3`` in Dockerfile.
-   Did some research about how to control pip.  My starting point was
    `What Are Python Wheels and Why Should You Care? <https://realpython
    .com/python-wheels/>`_, an article in this week's ``PyCoder's Weekly``
    email newsletter.

    -   I added a file called ``manage_requirements.txt`` to add parameters
        that I didn't want wiped out every time I updated
        ``requirements.txt``.
    -   In the ``manage_requirements.txt`` I added commands to force pip to
        only use wheels (binaries).  If an appropriate wheel is not found, it
        reports an error.

-   Ultimately, I commented out the uWSGI requiremnt since it will not be
    needed for this demo.

Finally, I was able to run the command::

    docker-compose up -d --build

The migrate command worked without tinkering.

The command to get a look at postgres got me in.  However, the command(s) to
enter at the ``hello_django_dev=#`` prompt are different than what is shown
in the tutorial.

-   The command to list all databases is ``\l`` (backslash el).
-   Connecting to a database is as listed: ``\c <database name>``.
-   Showing the table in the database ``\dt`` works.
-   The command to bail out ``\q`` works.

Inspecting the database volume did not work as written, apparently because I
named my project directory differently.  To get a list of valid volume names
use the command::

    docker volume ls

After determining the correct volume name, enter the following command::

    docker volume inspect <volume name>

I added the ``entrypoint.sh`` script, marked it executable, and modified the
``Dockerfile`` to use it.  I added the DATABASE variable to the ``.env.dev``
file.

After downing the prevously running containers and up building again, the
setup died because the nc command did not exist.  I tried:

-   Switching the FROM to both "python:3" and "python:3.8.3-alpine", but
    neither had the nc command.
-   After searching on the web for the Alpine image, I found that
    "alpine:3.7" ws available.  I gave that a try.  This time, the nc
    command was found.  However, I had to change a few more things to get
    everything to work.

    -   I reenabled the apk command and switched pip to to ``--prefer-binary``.
    -   The pip and python commands were not found but I noticed that pip3
        and python3 were installed as part of the startup, so I changed the
        appropriate places in ``Dockerfile``, ``entrypoint.sh`` and
        ``docker-compose.yaml``.

After these changes, I was able to get the browser to show the debug page
again.

I tried the to run the commands in the "Notes" section, but it failed.  I
didn't bother with trying to find out why.

******************************************************************************
04-SeparateDevProd - Notes
******************************************************************************

I diverted at this point to try to understand more of the defaults.  To
ensure that I got most of them, I copied the original files to ones ending
in "`.dev`" (or in some cases near the end).  I then movee the original
files out of the project and started running things again to see what failed.

After numerous failures and reading the documentation for Docker, I came up
with a revised set of files that work.  I also created scripts to build,
run, and stop the dev Docker containers.

After extensive searching on my Mac, I finally found where the containers
are kept. They are in ``~/Library/Containers/com.docker
.docker/Data/vms/<n>``.  I found it by using a program called "WhatsOpen"
and searching for Docker.  I could have used the linux utility lsof to do
the same thing.

I found out that the network name cannot have an underscore in it.

Apparently there is some place where the database name is determined other
than ``.env.dev``.  The file ``.env.dev`` must match whatever name the
database happens to have.

I commited all changes at this point.  I also created a chapter below called
`Handy Commands`_ to track the useful commands  that I found myself
using frequently.

After numerous attempts and fixes, I got prod to work.  Again I had to
modify the database name to just hello_django to make it work.

Note - the entry point script does not flush or migrate any more.  I have to
do that manually.

I used manage.py createsuperuser to put myself in the database.  Once I did
that I was able to use a "/admin" suffix to the url to get into the
administration pages.

Committing the changes and going on to a new branch.


******************************************************************************
Handy Commands
******************************************************************************

Handy Commands Cheatsheet
==============================================================================

docker info
    shows that the docker deamon is running and info about it

docker ps
    shows running docker containers

docker container ps
    shows running docker containers

docker network ls
    show active network names

docker images
    shows active and recent images

docker-compose -f <YAML file> --project-name <project name> build
    build a collection of containerx

docker-compose -f <YAML file> --project-name <project name> up -d --build
    build and start a collection of containers

docker-compose -f <YAML> down -v
    stop the collection of running containers

docker stop <container name>
    stop a specified container

docker rm <container name>
    removed a stopped container.

docker network rm <network name>
    removed a network

docker image prune
    removed unattached images

docker image rm <image id>

docker exec <container name> <cmd> [<parm> ...]
    execute one command in the container and view its output e.g.
    ``docker exec dev_db psql --username=hello_django --list``

docker exec -ti <container name> <cmd> [<parm> ...]
    run a command in the container interactively e.g.
    ``docker exec -ti dev_db psql --username=hello_django --dbname=hello_django``

docker-compose -f <YAML file> exec <service name> <cmd> [<parm> ...}
    run a command interactively in a container identified by service name e.g.
    ``docker-compose -f docker_compose.dev.yaml exec db psql --username=hello_django --dbname=hello_django``

docker logs <container name>
    displays a copy of the log file in the container


Handy Docker Commands
==============================================================================

These are some handy docker commands::

    docker [OPTIONS] COMMAND [ARGS...]

In the individual command documentation is appears that the OPTIONS are
immdeiately **after** the COMMAND.  However, the OPTIONS listed for the
commands below are actually the ARGS listed above.  Confusing, but that is
how it is.

Docker Options
==============================================================================

Options are generic to docker rather than being specific to a specific
command.  On the other hand, args vary by command.

-   \--config string                    string = (unknown)

-   \-c, --context string               string = (unknown)

-   \-D, --debug                        enable debugging mode

-   \--help                             compact description of command and args

-   \-l, --log-level                    sets log level ("debug", etc.)

Docker Commands - Useful
==============================================================================

The following docker commands are ones I found useful.  Note that adding one
of the options above may be helpful.

docker ps
------------------------------------------------------------------------------

Shows all running docker containers.

``docker ps --all`` shows all containers known, even if they are not active.

``docker ps --no-trunc`` does not truncate any column of output.

``docker ps --size`` shows the size of each container

There are other options for more specialized uses.

docker attach
------------------------------------------------------------------------------

Attaches the std in, std out, and std err to the terminal for live output
from the running container.

``docker attach [OPTIONS] CONTAINER``   generic form

CONTAINER may be the container ID or its name.

See the documentation before using.

docker container
------------------------------------------------------------------------------

Manages containers.  Containers can be specified by either container id or
name.

``docker container ls``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lists all active containers

``docker container inspect CONTAINER``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Provides a **huge** amount of output

``docker container start  [OPTIONS] CONTAINER [CONTAINER...]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Starts one or more containers.

``docker container stop  [OPTIONS] CONTAINER [CONTAINER...]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stops one or more containers.

``docker container kill [OPTIONS] CONTAINER``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Immediately stops a running container

``docker container pause CONTAINER [...]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Freeze a container (from executing)

``docker container unpause CONTAINER [...]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Resumes a paused container

``docker container restart [OPTIONS] CONTAINER``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Restarts a container (perhaps a shortcut for a stop - start sequence)?

``docker container prune [OPTIONS]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Remove all stopped containers

``docker container rm  [OPTIONS] CONTAINER``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Removes a container from docker

``docker container exec [OPTIONS] CONTAINER [...] COMMAND [ARG...]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Submits a command for execution on the specified container(s).

ARG may be:

    -d, --detach    runs the command detached from the terminal
    -e, --env       set environment variables
    --privileged    give extended privileges to the command in the container
    -u, --user      username used inside the container
    -w, --workdir   working directory inside the container

    Other options available

``docker container export [OPTIONS] CONTAINER``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creates a zip archive of the filesystem inside the container.

OPTIONS may be:

    -o, --output    specifies a file name for the zip archive rathet than
                    std out

``docker container logs [OPTIONS] CONTAINER``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Show logs from a container

OPTIONS:

    -f, --follow    like tail -f
    --details       show addional information
    --tail n        shows n lines from the end (default is to show all lines)

    Other options available

``docker container port CONTAINER``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

List open ports (like nmap)

``docker container stats [OPTIONS] [CONTAINER]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Collect a stream of stats from one or more containers.

OPTIONS:

    --no-stream     Collect and display one shot of stats, then quit.
    --no-trunc      Don't truncate any columns.
    -a, --all       Show stats from non-running containers as well.

``docker container top CONTAINER [ps OPTIONS]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Shows the top processes in a container.

docker diff
------------------------------------------------------------------------------

Show the difference in files since the container was created.

``docker diff CONTAINER``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Shows each different file or directory in the container with "A" - added,
"C" - changed in some way, "D" - deleted.

docker exec
------------------------------------------------------------------------------

Execute a given single command in the specified container.

``docker [OPTIONS] exec CONTAINER COMMAND [ARG...]``

OPTIONS:

    -w, --workdir   sets working directory inside container
    -u, --username  username to use within the container
    --privileged    runs commmand with privileged status in container
    -d, --detach    runs command in container in the background

docker export
------------------------------------------------------------------------------

Export a container as a tar archive.

``docker export [OPTIONS] CONTAINER

OPTIONS:

    -o, --output    names file to contain tar file instead of stdout

docker history
------------------------------------------------------------------------------

Show the history of an image.

``docker history [OPTIONS] IMAGE``

Options available

docker image
------------------------------------------------------------------------------

Multiple subcommands to manage an image similar to docker container.
Subcommands include: build, **history**, import, inspect, load, **ls**,
**prune**, pull, push, **rm**, save and tag.

docker images
------------------------------------------------------------------------------

List docker images.  Options include specifying the repository, showing size
and tags, digest format, filtering,

docker import
------------------------------------------------------------------------------

Import an image previously created by docker export.

docker info
------------------------------------------------------------------------------
Displays system-wide Docker info including version, total number of
containers and the status counnts, etc.

docker kill
------------------------------------------------------------------------------

Sends a signal to the named container to bring it down somewhat abruptly.

docker load
------------------------------------------------------------------------------

Load and image from a specified tar file (or other compressed image).

docker logs
------------------------------------------------------------------------------

Retrieve the logs of the specified container.

``docker logs [OPTIONS] CONTAINER

OPTIONS:

    -f, --follow    like tail -f
    --details       show addional information
    --tail n        shows n lines from the end (default is to show all lines)

    Other options available

docker network
------------------------------------------------------------------------------

Manage docker networks

``docker network connect --alias <alias name> CONTAINER``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assign and alias to a container to disambiguate container references.

``docker network inspect [OPTIONS] NETWORK [NETWORK...]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Inspect one or more docker networks.


docker node
------------------------------------------------------------------------------

docker pause

docker plugin

docker port

docker pull

docker push

docker registry

docker rename

docker restart

docker rm

docker rmi

docker run

docker save

docker search

docker secret

docker service

docker stack

docker start

docker stop

docker stats

docker system

docker tag

docker top

docker trust

docker unpause

docker update

docker volume

docker wait

Docker Commands - Less Useful
==============================================================================

These command were less useful to me.

docker app - (marked experimental)

docker build - use docker-compose instead

docker builder - a way of invoking docker build or to prune build cache

docker buildx - (marked experimental)

docker checkpoint - (marked experimental)

docker config - useful only for swarms

docker container run IMAGE - runs a command in a **new** container (has
tons of options)

docker container update - updates the configuration of a container

docker container wait - blocks until one or more containers stop, then
prints their exit code.

docker context - manage contexts (useful for swarms and Kubernetes

docker cp - copy a container

docker create - create a container, but not start it.

docker events - show real-time events for containers, images, networks, etc.

docker inspect - show a huge amount of info -- if you can supply the proper
identifier.

docker login - login to a registry server, such as Docker Hub.

docker logout - logout of a registry server, such as Docker Hub.

docker manifest - experimental









Section

Official list of Python heading levels

    - # with overline, for parts
    - \* with overline, for chapters
    - = for sections
    - \- for subsections
    - ^ for subsubsections
    - " for paragraphs


Blah blah *italics*  **bold**

This is a numbered list

    1. Numbered items
    #. Numbered items
    #. Period can be replaced by a dash, right paren, etc., but is 
       required.  A continuation must be indented the same as the number.

This is a bulleted list
    - Bulleted items
    - Bulleted items
    
        - sublist items

Show an indented literal text block like this:

::

    literal text
    ...

Text indented the same as the "::" marker ends the literal text

A simple sample Table

============   ========================
Cell Title     Another Cell  Title
============   ========================
contents       more contents
item 1         item 2
green          purple
============   ========================

A grid table

+---------------+--------------+--------------+
| Header Col 1  | Header 2     |   Centered   |
| Extended      |              |   Header     |
+===============+==============+==============+
| Body 1        |   Body 2     |       Body 3 |
+---------------+--------------+--------------+
| Left Just     |   Centered   |   Right Just |
+---------------+--------------+--------------+
| This entry spans these cols  | This entry   |
+---------------+--------------+              +
| Blah          | Blah         | spans rows   |
+---------------+--------------+--------------+

Link to external URL: `Apple main web site <http://www.apple.com>`_ that way.

Reference to a reference elsewhere in the same document:  `Link to elsewhere`_

Blah blah

    _`Link to elsewhere`   <-- This is the target of the link above.

To reference another document use ::

    :doc:`title <doc name and location>`

    Must not be a space between the : and the backtick!

    Can also use :any: - it will try to do :doc:, :ref:, etc.

        If not found, will then try to find a Python object with that name
        and link to it (e.g. class name, function name, module name, etc.)

Glossary-type definition
    The definition for the term must be indented and immediately below
    the term.

    Blank lines may appear in the definition body, but must not
    come between the term and the first line of definition.

    The term defined can be referenced elsewhere by :term:,
    e.g. :Glossary-type definition:
