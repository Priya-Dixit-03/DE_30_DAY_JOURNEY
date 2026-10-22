from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='weather_pipeline_IDR',  
    default_args=default_args,
    description='A simple weather ETL pipeline (Extract -> Transform -> Load)',
    schedule_interval=None,  
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['weather', 'etl'],
) as dag:

    # Task 1: Extract Weather Data
    extract_task = BashOperator(
        task_id='extract_weather',
        bash_command='python /opt/airflow/project_etl/extract.py',
    )

    # Task 2: Transform Weather Data
    transform_task = BashOperator(
        task_id='transform_weather',
        bash_command='python /opt/airflow/project_etl/transform.py',
    )

    # Task 3: Load Weather Data into Neon Database
    load_task = BashOperator(
        task_id='load_weather',
        bash_command='python /opt/airflow/project_etl/load.py',
    )

    # Define task pipeline dependencies
    extract_task >> transform_task >> load_task