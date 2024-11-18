from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

with DAG(dag_id='bronze_to_silver',
         start_date=datetime(2023, 1, 1),
         schedule_interval='@once',
         catchup=False) as dag:
    run_dbt = BashOperator(
        task_id='run_dbt_bronze',
        bash_command='dbt run --models bronze'
    )
    test_dbt = BashOperator(
        task_id='test_dbt_bronze',
        bash_command='dbt test --models bronze'
    )
    
    run_dbt = BashOperator(
        task_id='run_dbt_silver',
        bash_command='dbt run --models silver'
    )
    test_dbt = BashOperator(
        task_id='test_dbt_silver',
        bash_command='dbt test --models silver'
    )
    trigger_next_dag = TriggerDagRunOperator(
        task_id='trigger_silver_to_gold',
        trigger_dag_id='silver_to_gold'
    )
    run_dbt >> test_dbt >> trigger_next_dag
