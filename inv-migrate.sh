#!/usr/local/bin/bash

# Purpose: Run the database migration in the prod environment

# Get constants for project
source inv.project-constants.prod

{
  cd $ROOT
	docker-compose -f $YAML_FILE --project-name $PROJECT exec $WEB_SERVICE_NAME python manage.py flush --no-input
	docker-compose -f $YAML_FILE --project-name $PROJECT exec $WEB_SERVICE_NAME python manage.py migrate --no-input
} 2>&1 | tee ./log/${0}.log

# EOF

