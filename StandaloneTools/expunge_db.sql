SELECT *
FROM pg_stat_activity
WHERE datname = 'test_WARM';

SELECT pg_terminate_backend (pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'test_WARM';

SELECT *
FROM pg_stat_activity
WHERE datname = 'template1';

SELECT pg_terminate_backend (pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'template1';

DROP DATABASE IF EXISTS "test_WARM";

