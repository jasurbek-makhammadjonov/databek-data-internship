from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime

from scripts.load_orders import load_yesterday_orders


with DAG(
    dag_id="daily_revenue_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    load_stage = PythonOperator(
        task_id="load_yesterday_orders",
        python_callable=load_yesterday_orders
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/dbt && dbt run"
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/dbt && dbt test"
    )

    load_stage >> dbt_run >> dbt_test