#!/bin/bash


sudo -u postgres psql -c "DROP DATABASE \"WARM\""

sudo -u postgres psql -c "CREATE DATABASE \"WARM\""

./manage.py migrate

./manage.py createsuperuser

./manage.py loaddata \
  LocBin \
  LocRow \
  LocTier \
  ProductCategory \
  Product \
  Location \
  BoxType \
  Constraints






