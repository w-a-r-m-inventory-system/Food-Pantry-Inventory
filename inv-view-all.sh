#!/usr/local/bin/bash

# Purpose: See all docker containers, volumes, networks, and images.

# get all the docker constants
source inv.project-constants.prod

{
  echo "All running docker tasks..."
  docker ps --all
  echo
  echo "All containers..."
  docker-compose -f $YAML_FILE --project-name $PROJECT ps --all
  docker container ps --all
  echo
  echo "All docker networks..."
  docker network ls
  echo
  echo "All docker volumes..."
  docker volume ls
  echo
  echo "All docker images..."
  docker images
} 2>&1 | tee log/${0}.log

# EOF
