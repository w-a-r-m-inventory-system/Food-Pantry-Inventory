# Install Food Pantry Inventory Project 

These instructions are designed to help someone who has never had the food
pantry project installed on their system.  For those who have had some
version of the project installed (and perhaps running) before, skip down to
the appropriate steps and resume from that point.

Although these instructions are straightforward, they also discuss actions
at a fairly high level.  If a step assumes more knowledge than you happen
to have, please refer to any of:

-   https://food-pantry-inventory.readthedocs.io/en/latest/
-   <Project Directory>/docs/source (may be slightly newer than the URL above)
-   https://github.com/w-a-r-m-inventory-system/Food-Pantry-Inventory/wiki
-   Any of the other members of the project team who happen to have more
    experience with that aspect of the project.
-   Vendor documentation -- as appropriate.
-   General internet search.

These instructions were prepared in July 2020.  Obviously, as time goes by,
they will be increasingly out-of-date.  

## Assumptions

These instructions assume that these have been installed and configured:

-   Python 3.6 or newer
-   PyCharm - current Professional or Community edition
-   git
-   PostgreSQL

To pull down a specific branch, use
    ```git clone -b (branch name) https://github.com/deeppunster/Food-Pantry-Inventory.git```

To have full functionality these tools are needed (but not required):

-   nginx
-   uWSGI (included in requirements.txt)
-   graphviz
-   LaTeX tools

## Install Project Base Instructions

1.  Obtain the URL for the project from the main repository

2.  Using PyCharm, create a project directory - preloading git using the URL
 from the previous step

3.  Create a virtual environment for the project.

    -   The directories venv and .venv are already ignored by git.
    
4.  Load the needed libraries indicated by the requirements.txt file.

    -   At this time, the latest pendulum library (2.1.1) requires PEP 517 for
     it to build its wheel.  However, the changes PEP 517 makes to the pip
     program have not been incorporated into the pip for the most recent
     released version of Python (3.8).
     
     -  pendulum 2.1.0 requires version 1.4.* of the library lazy-object-proxy 
     rather than the current 1.5.0.

5.  Create the directory FPIDjango/private

6.  Copy FPIDjango/settings_private.py to the new private directory.

7.  Tailor the FPIDjango/private/settings_private.py file to the local
    environment for this project.
 
    -   The database is assumed to be named "WARM" (in all upper case).
    
    -   If you don't happen to be good at coming up with 50 random hex digits,
        there is a program in StandaloneTools called GenerateSecretKey.py
        that will do the job.
    
8.  Run the script named drop_and_rebuild_db.sh.

9.  Run the Python program setup_warm_groups.py
        
## Test Project Base Instructions
    
1.  Test the system manually by running the shell script:

    ```./run_inv```
    
2.  When done testing, kill the server started in the previous step.

3. Run automated testing of the system by running the shell script:

    ```./run_pytest```
    
## Generate Documentation Instructions

1.  To generate html documentation run the shell script:

    ```./mkdoc```

-    Parts of this script will fail if graphviz is not installed.
    
2.  To generate pdf documentation run the shell script:

    ```./mkdoc latexpdf```

-    This script will fail if the LaTeX tools are not installed.


## Coordinating nginx and uWSGI

Note that it does not matter whether you start up nginx or uwsgi
first, as long as they are able to talk to each other.vim :

For nginx and uWSGI to communicate successfully, the server and port
specified by the __-socket__ parameter in the uwsgi command line must match
the __uwsgi_pass__ parameter on line 42 of the __nginx.conf__ file.

The application can be accessed by constructing a URL from the server
(pointed to by the server specified by the __server_name__ parameter on line
36), and the port (specified by the listen parameter on line 36) of the
__nginx.conf__ file.

## Install and Use nginx

-   This requires that nginx be installed on the execution path of the project.

-   The nginx.conf can be configured any number of ways and will depend on
    the local operating system. See the other instructions, **nginxconf.md**
    for help with the file. 

1.  Prepare static files for nginx:

    ```./manage.py collectstatic```
    
-   This will copy all the static files found in any app in the Django
    project to the directory specified by the __STATIC_ROOT__ variable in
    your __settings_private.py__ file.
    
-   These instructions assume that you have specified the ```./static```
    directory at the root of this project.
    
2.  Modify the __nginx.conf__ in the directory ```./config/nginx``` 
    directory if needed.
    
3.  To start nginx run the shell script (may need to run with sudo):

    ```./run_nginx```
    
-   The same script can be used to test any changes to the conf file, quit
    nginx, or tell nginx to reload its parameters from a (presumably) 
    revised conf file.
    
## Install and Use uWSGI

-   This requires that the library uWSGI has been successfully installed as
    part of the requirements for the project.

1.  To start uWSGI run the bash script:

    ```./start_uswgi```
    
2.  To stop the uWSGI daemons, run the bash script:

    ```./stop_uwsgi```
    

        
## Post-installation Comments

-   Always use the ``User Management`` screen to add or update users.  This
    will ensure that the appropriate profile record is created and maintained
    for the user.

