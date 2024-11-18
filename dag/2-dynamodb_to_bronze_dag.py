from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.dynamodb import DynamoDBHook
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from utils.utils import BRONZE_LAYER_PATH, AWS_CONN_ID, KAFKA_TOPIC, S3_BUCKET_NAME
import pandas as pd
from datetime import datetime

def export_dynamodb_to_s3():
    dynamo_hook = DynamoDBHook(aws_conn_id=AWS_CONN_ID)
    records = dynamo_hook.scan(table_name=KAFKA_TOPIC)
    df = pd.DataFrame(records)
    # Save as Parquet file
    df.to_parquet('/tmp/bronze_layer.parquet')
    s3_hook = S3Hook(aws_conn_id=AWS_CONN_ID)
    s3_hook.load_file('/tmp/bronze_layer.parquet', BRONZE_LAYER_PATH , bucket_name=S3_BUCKET_NAME, replace=True)

with DAG(dag_id='dynamodb_to_bronze',
         start_date=datetime(2023, 1, 1),
         schedule_interval='@once',
         catchup=False) as dag:
    export_to_bronze = PythonOperator(
        task_id='export_dynamodb_to_s3',
        python_callable=export_dynamodb_to_s3
    )

    trigger_next_dag = TriggerDagRunOperator(
        task_id='trigger_bronze_to_silver',
        trigger_dag_id='bronze_to_silver'
    )
    export_to_bronze >> trigger_next_dag
