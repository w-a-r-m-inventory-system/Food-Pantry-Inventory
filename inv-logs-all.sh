#!/usr/local/bin/bash

# Purpose: List the logs for prod

# Get constants for project
source inv.project-constants.prod

{
  docker-compose -f $YAML_FILE --project-name $PROJECT logs -f
} 2>&1 | tee log/${0}.log

# EDF
