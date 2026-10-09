#!/usr/bin/env bash
set -euo pipefail

psql --set ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
    --set airflow_user="$AIRFLOW_DB_USER" \
    --set airflow_password="$AIRFLOW_DB_PASSWORD" \
    --set airflow_database="$AIRFLOW_DB_NAME" <<'SQL'
SELECT format('CREATE USER %I WITH PASSWORD %L', :'airflow_user', :'airflow_password')
WHERE NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = :'airflow_user') \gexec

SELECT format('CREATE DATABASE %I OWNER %I', :'airflow_database', :'airflow_user')
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = :'airflow_database') \gexec
SQL
