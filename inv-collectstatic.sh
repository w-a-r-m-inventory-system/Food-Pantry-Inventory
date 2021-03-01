#!/usr/local/bin/bash

# Purpose: Collect the static files in the prod environment

# Get constants for project
source inv.project-constants.prod

{
	docker-compose -f $YAML_FILE --project-name $PROJECT exec $WEB_SERVICE_NAME python manage.py collectstatic --no-input
} 2>&1 | tee ./log/${9}.log

# EOF

