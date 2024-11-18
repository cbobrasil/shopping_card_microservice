from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from utils.utils import S3_BUCKET_NAME, KAFKA_CONN_ID, AWS_CONN_ID, KAFKA_TOPIC, BRONZE_LAYER_PATH
from datetime import datetime

with DAG(dag_id='silver_to_gold',
         start_date=datetime(2023, 1, 1),
         schedule_interval='@once',
         catchup=False) as dag:
    run_dbt = BashOperator(
        task_id='run_dbt_gold',
        bash_command='dbt run --models gold'
    )
    trigger_next_dag = TriggerDagRunOperator(
        task_id='trigger_gold_to_redshift',
        trigger_dag_id='gold_to_redshift'
    )
    run_dbt >> test_dbt >> trigger_next_dag
