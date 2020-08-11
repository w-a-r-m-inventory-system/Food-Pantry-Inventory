#!/bin/bash

# Drop the test database in spite of others connected to it.
psql -d WARM -f expunge_WARM_db.sql

# EOF

