#!/usr/local/bin/bash

# Purpose: Peek into the dockerized database for prod environment

# Get constants for project
source inv.project-constants.prod

echo 
echo "    \l, \list to list the databases"
echo "    \dt to list the tables in the prod database"
echo "    \quit to leave psql"
echo

{
  docker-compose -f $YAML_FILE --project-name $PROJECT exec $DB_SERVICE_NAME psql --username=$USER_NAME --dbname=$DB_NAME
} 2>&1 | tee log/${0}.log

# EOF
