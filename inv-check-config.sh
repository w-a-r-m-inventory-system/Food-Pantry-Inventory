#!/usr/local/bin/bash

# Purpose: Check  the configuration of the YAML file for validity

# Get constants for project
source inv.project-constants.prod

{
  docker-compose -f $YAML_FILE config
} 2>&1 | tee ./log/${0}.log

# EOF

