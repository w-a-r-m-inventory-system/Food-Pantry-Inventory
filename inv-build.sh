#!/usr/local/bin/bash

# Purpose: run docker-compose build for prod

# Get constants for project
source inv.project-constants.prod

{
  docker-compose -f $YAML_FILE --project-name $PROJECT build
} 2>&1 | tee ./log/${0}.log

# EOF
