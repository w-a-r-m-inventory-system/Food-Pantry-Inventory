#!/usr/local/bin/bash

# Purpose: Clear all newly created docker containers, volumes, networks, and
# images.

# get all the docker constants
source inv.project-constants.prod

{
  echo "Clear all running docker tasks and containers..."
  ./inv-stop.sh
  docker container prune
  echo
  echo "Clear all docker networks..."
  docker network rm $NETWORK_NAME
  echo
  echo "Clear all docker volumes..."
  docker volume prune
  echo
  echo "Clear all locally created docker images..."
  echo "(takes more logic than I have time for)"
  docker image prune
  docker images
} 2>&1 | tee log/${0}.log

# EOF
