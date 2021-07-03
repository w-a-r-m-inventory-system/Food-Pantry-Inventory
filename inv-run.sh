#!/usr/local/bin/bash

# Purpose: Run the previously built docker conntainer(s) for prod

# Get constants for project
source inv.project-constants.prod

{
  docker-compose -f $YAML_FILE --project-name $PROJECT up -d
} 2>&1 | tee ./log/${0}.log

