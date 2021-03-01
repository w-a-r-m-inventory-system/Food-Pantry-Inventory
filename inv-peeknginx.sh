#!/usr/local/bin/bash

# Purpose: Peek into the dockerized nginx container for prod environment

# Get constants for project
source inv.project-constants.prod

echo "Static files are at /home/app/web/staticfiles"
echo "Media files are at /home/app/web/mediafiles"

{
  docker-compose -f $YAML_FILE --project-name $PROJECT exec $NGINX_SERVICE_NAME sh
} 2>&1 | tee log/${0}.log

# EOF
