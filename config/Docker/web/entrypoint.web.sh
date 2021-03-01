#!/bin/sh

# explore reason for not coming up
id
pwd
echo 'Listing of current directory'
ls -l .
echo '\nListing of FPIDjango'
ls -l FPIDjango
echo 'Listing of certain commands'
which python
python --version
python manage.py  check
python manage.py  check fpiweb


if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

#     while ! nc -z $SQL_HOST $SQL_PORT; do
    while ! python netcat.py $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"

