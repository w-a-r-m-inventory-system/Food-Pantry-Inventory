#!/bin/sh 

# shell script to run pytest from the top of the inventory project
# 
# Usage:
#        run_pytest
#                    runs pytest on project with no "coverage"
#
#        run_pytest -n n
#                    runs pytest using n cores (faster)
#
#        run_pytest -c pytest_w_cov.ini
#                    runs pytest with coverage
#
#        run_pytest -n n -c pytest_w_cov.ini
#                    runs pytest with multiple cores and coverage

# Activate the virtual environment if needed
if [ X = X`echo deactivate` ]
then
    source VIRTUAL_BIN_LOCATION/activate
fi

# identify location of the setting file for Django
export DJANGO_SETTINGS_MODULE=FPIDjango.settings

# assume pytest is in the current path
# add "-n 4" on the command line to use four cores for the tests 
pytest "$@" -ra --fail-on-template-vars

# EOF

