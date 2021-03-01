#!/usr/local/bin/bash

# Purpose: stop currently running docker containers for prod

# Get constants for project
source inv.project-constants.prod

{
  docker-compose -f $YAML_FILE --project-name $PROJECT down
} 2>&1 | tee ./log/${0}.log

# EOF

