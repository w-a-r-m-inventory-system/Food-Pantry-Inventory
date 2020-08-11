#!/bin/bash
# start the uWSGI server
uwsgi --socket 127.0.0.1:9876 --wsgi-file FPIDjango/wsgi.py --master --processes 4 --threads 2 --stats 127.0.0.1:9870 &
