import pendulum
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from api_etl.__main__ import main


with DAG(
    dag_id="api_etl_dag_orchestrator",
    description="Run the API ETL pipeline",
    start_date=pendulum.datetime(2026, 10, 8, tz="Europe/London"),
    catchup=False,
    schedule=timedelta(hours=1),
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    }
) as dag:
    run_etl = PythonOperator(
        task_id="run_etl",
        python_callable=main,
    )