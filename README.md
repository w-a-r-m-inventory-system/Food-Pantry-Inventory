# Food Pantry Inventory Tracking

[![Documentation Status](https://readthedocs.org/projects/food-pantry-inventory/badge/?version=latest)](https://food-pantry-inventory.readthedocs.io/en/latest/?badge=latest)

Welcome to the Food Pantry Inventory open source project!

This project is designed to track the inventory in the warehouse of a food
pantry.  It tracks boxes of product by location (row, bin, and  tier), contents
(green beans, corn, etc.) and by expiration year.  The expiration can 
optionally be tracked by half-year, quarter, or arbitrary month ranges.

Details of this system are given in the documentation located at docs/source/index.rst.

## Code of Conduct

Code of conduct for this project is given in 
[Code of Conduct](Code_of_Conduct.md).

## Licensing

This project is licensed following the MIT licene given in
[License](LICENSE),

## Contributors

Contributors are noted in [Contributors](Contributors.md)

# Quick Start Install

1.  Download the zip file for the master branch of this project.

2.  Unpack the zip file in a convenient directory.

3.  Create a python virtual environment for this project.

    e.g. virtualenv venv 
    while in the root directory of the project, and then 
    source venv/bin/activate
    to activate the venv
    
4.  Install the various libraries needed.

    pip3 install -r requirements.txt
    
    Note: if you are on Windows 10 and only plan to run it locally, then remove uWSGI and change Pendulum to 2.0.3 in order for             all the requirements to successfully install. 
    
5.  Note - this project defaults to using PostgreSQL.  If you choose to use
some other database, now would be a good time to install any additional
libraries to support it.

6.  Create a directory "./FPIDjango/private" and copy 
./FPIDjango/private_settings.py to ./FPIDjango/private/private_settings.py.

    Note that the .gitignore file is set to ignore anything in the 
    ./FPIDjango/private subdirectory.
    
7.  Create a database and start a server for it.  The tables in the database
will be created in a later step.  Make a note of the database name, the
 server access (host, port, etc.), and credentials for a user that can
  modify the schema for the database. 

8.  Modify ./FPIDjango/private/private_setting.py file to taste.

    a.  DB_ENGINE - set to the appropriate backend for your database.
    
    b.  DB_NAME - set to the database name to use for this project.
    
    c.  DB_USER - the user name from the credentials that can modify the
    schema for this database.
    
    d.  DB_PSWD - the password for the DB_USER above.
    
    e.  DB_HOST - the IP or URL to reach the database server.
    
    f.  DB_PORT - the port the server is using to listen for requests.
    
    g.  MY_SECRET_KEY - a random string of 50 bytes or more.
    
        If you wish, use the program ./StandaloneTools/GenerateSecretKey.py
        for this.
        
9.  Populate the database with all the tables needed by going to the
main directory and running:

    ./manage.py migrate
    
    If all went well, your database should now have a bunch of tables
    starting with auth*, django*, and fpiweb*.
    
10. At this time the inventory system is ready to use.

    a.  To start the inventory system, use "run_inv" to start running it.
        
    b.  To test the inventory system, use "run_pytest" to run all the django
        unit tests and the pytests contained in the "tests" subdirectory.
        
    c.  An alternate way to run the tests is to run the following commands.
    
        source venv/bin/activate            (if this has not already been run)
        
        ./manage.py test

## How to Get Started Contributing

Please refer to the Wiki for this project on how to get set up to contribute
to this project.
