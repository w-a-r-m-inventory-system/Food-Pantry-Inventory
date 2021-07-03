#!/usr/local/bin/bash

# Purpose: Show evidence that the various volumes were created

# get all the docker constants
source inv.project-constants.prod

{
  echo "Inspect static volume..."
  docker volume inspect $STATIC_FILE_VOLUME
  echo
  echo "Inspect database volume..."
  docker volume inspect $DB_DATA_VOLUME
  echo
  echo "Inspecting media volume..."
  docker volume inspect $MEDIA_FILE_VOLUME
} 2>&1 | tee ./log/${0}.log

# EOF

