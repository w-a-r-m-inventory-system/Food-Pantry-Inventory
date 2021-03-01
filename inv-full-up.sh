#!/usr/local/bin/bash

# Purpose: Run all steps to get everything in place for inv

# Get constants for project
source inv.project-constants.prod

{
  ./inv-run.sh
  ./inv-migrate.sh
  ./inv-adddata.sh
  ./inv-collectstatic.sh
  ./inv-adduser.sh
} 2>&1 | tee ./log/inv-full-up.log

# EOF

