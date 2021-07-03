#!/usr/local/bin/bash

# Purpose: Run the database started data in the prod environment

# Get constants for project
source inv.project-constants.prod

# list of fixtures to be added to a completely empty database
LOCATION_FIXTURES="LocRow LocBin LocTier Location"
PRODUCT_FIXTURES="Product ProductCategory ProductExample"
OTHER_FIXTURES="BoxType Constraints Group"
FIXTURE_LIST="$LOCATION_FIXTURES $PRODUCT_FIXTURES $OTHER_FIXTURES"

{
  echo "Starting to load fixtures..."
  cd $ROOT
	docker-compose -f $YAML_FILE --project-name $PROJECT exec $WEB_SERVICE_NAME python manage.py loaddata --app fpiweb $FIXTURE_LIST
  echo "Loading fixtures complete"
} 2>&1 | tee ./log/${0}.log

# EOF

