from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="hello_priya",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
) as dag:
    t1 = BashOperator(task_id="say_hello", bash_command="echo 'Hello Priya, Airflow is working!'")
    t2 = BashOperator(task_id="say_done", bash_command="echo 'Task completed successfully!'")
    t1 >> t2