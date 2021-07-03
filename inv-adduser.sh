#!/usr/local/bin/bash

# Purpose: Add a superuser to the dockerized database for prod environment

# Get constants for project
source inv.project-constants.prod

{
	echo "Please provide a password for the inital superuser at the next prompt..."
	docker-compose -f $YAML_FILE --project-name $PROJECT exec $WEB_SERVICE_NAME python manage.py createsuperuser --username=$USER_NAME --email=$EMAIL
} 2>&1 | tee log/prod-add-user.log

# EOF
