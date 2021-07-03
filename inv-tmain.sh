#!/bin/bash

# Purpose: test prod main web site via html

# Get constants for project
source inv.project-constants.prod

{
  open "http://localhost:1337"
} 2>&1 | tee ./log/${0}.log

# EOF
