#!/bin/bash

# bash (only) shell script to run the Django-based inventory system

# General assumptions:
# - The virtual environment is located in a subdirectory called "venv".
# - This script is located at the root level of the inventory system directory.
#- manage.py is also located at the root level of the inventory system.

# Script Assumptions:
ROOT=$(pwd)
MANAGE_LOCATION=$ROOT
MANAGE_CMD=$MANAGE_LOCATION/manage.py
VIRTUAL_BIN_LOCATION=$ROOT/venv/bin
PYTHON=$VIRTUAL_BIN_LOCATION/python
LOG_LOCATION=$ROOT/log
LOG_FILE=$LOG_LOCATION/server.log
HOST_IP=localhost
SERVER_PORT=8765

# Python environment variables
export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=FPIDjango.settings
export PYTHONPATH=$PYTHONPATH:$ROOT

# Activate the virtual environment if needed
if [ X = X"$(echo deactivate)" ]; then
  # shellcheck disable=SC1090
  source $VIRTUAL_BIN_LOCATION/activate
  echo "Virtual environment activated..." > $LOG_FILE
else
	echo "Virtual environment already set..." > $LOG_FILE
fi

# show all environment variables
myenv > $LOG_FILE > $LOG_FILE

# defines a task to run the Django server
# task is needed so we can tell which process to kill when done
run_server() {
  cd $LOG_LOCATION
  echo -e "Current PID is $$ " > $LOG_FILE
  $PYTHON $MANAGE_CMD runserver $HOST_IP:$SERVER_PORT 2>&1 | tee $LOG_FILE
}

# start Django server as a background task
# Note that this task will also be killed if the terminal session is closed
run_server &

# capture pid of the background tasks
ROOT_PID=$!
SERVER_PID=$(ps -f | grep runserver | awk "\$3 = $ROOT_PID { print \$2 }") >/dev/null 2>&1
echo -e "root: $ROOT_PID, task: $SERVER_PID" > $LOG_FILE

# wait a moment for the server to start up
sleep 2s

# build client URL
CLIENT_URL=http://$HOST_IP:$SERVER_PORT
# start a browser
if [ "$(uname)" = 'Darwin' ]; then
  # assume this is a Macintosh
  open $CLIENT_URL
elif [ "$X" = "Y" ]; then
  # identify Windows Subsystem for Linux (WSL) and run command to start URL
  cmd.exe /c start $URL
elif [ "$SHELL" = '/bin/bash' ]; then
  # Assume some form of Linux with xdg-open command
  xdg-open $CLIENT_URL
else
  echo -en "\n\tUnable to open the URL $CLIENT_URL for you.  "
  echo -e "Please open manually.\n"
  echo -en "\tIf/when you get tired of opening this URL manually, Please "
  echo -en "\timprove this script for your OS and submit a pull request.  :)"
fi

# tell user how to kill the server
echo  -e "\nInstead of typing a CONTROL-C to kill the server, type"
echo  -e "\tkill -QUIT $SERVER_PID (for Linux and Mac) "
echo  -e "instead when you are done with the server."

# EOF
