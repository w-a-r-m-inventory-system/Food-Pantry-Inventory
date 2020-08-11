SELECT *
FROM pg_stat_activity
WHERE datname = 'WARM';

SELECT pg_terminate_backend (pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'WARM';

SELECT *
FROM pg_stat_activity
WHERE datname = 'template1';

SELECT pg_terminate_backend (pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'template1';

DROP DATABASE IF EXISTS "WARM";

