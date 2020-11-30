#!/bin/bash

# manage the nginx server

# config file location
export CONFIG_LOCATION='/Volumes/MBPC/Dvl/Python/PythonProjects/Food-Pantry-Inventory/config/nginx/nginx.conf'
# for MacOS with nginx installed with Homebrew, the configuration file
# is located at /usr/local/etc/nginx/nginx.conf.

usage() 
{
	echo 'USAGE:'
	echo 'run_nginx [ quit | stop | reload | reopen | test ]'
	echo
	echo 'run_nginx (with no parameters) starts the server'
	echo
	echo 'run_nginx quit      graceful shutdown'
	echo 'run_nginx stop      fast shutdown'
	echo 'run_nginx reload    reload the configuration file'
	echo 'run_nginx reopen    reopen the log files'
	echo 'run_nginx test      verify the conf file and dump all nginx values'
}

# verify only one (or zero) parameters
if [ $# -gt 1 ]
then
	usage
	exit 1
elif [ $# -eq 1 ]
then
	parm=$1
fi

if [ "X$parm" = "X" ]
then
    nginx -c $CONFIG_LOCATION
elif [ "X$parm" = "Xtest" ]
then
    nginx -c $CONFIG_LOCATION -T
else
    nginx -c $CONFIG_LOCATION -s $parm
fi

# EOF

