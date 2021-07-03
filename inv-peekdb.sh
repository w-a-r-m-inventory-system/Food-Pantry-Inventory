#!/usr/local/bin/bash

# Purpose: Peek into the dockerized database container for prod environment

# Get constants for project
source inv.project-constants.prod

echo "Data is at /var/lib/postgresql/data/"

{
docker-compose -f $YAML_FILE --project-name $PROJECT exec $DB_SERVICE_NAME sh
} 2>&1 | tee log/${0}.log

# EOF
