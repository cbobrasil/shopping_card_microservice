from airflow import DAG
from airflow.operators.python import PythonOperator
from utils.utils import S3_BUCKET_NAME, KAFKA_CONN_ID, AWS_CONN_ID, KAFKA_TOPIC, BRONZE_LAYER_PATH
from datetime import datetime

# Function to load Gold Layer data into Redshift
def load_gold_to_redshift():
    print("Load Gold Layer data into Amazon Redshift.")

# DAG definition
with DAG(dag_id='gold_to_redshift',
         start_date=datetime(2023, 1, 1),
         schedule_interval='@once',
         catchup=False) as dag:
    load_to_redshift = PythonOperator(
        task_id='load_to_redshift',
        python_callable=load_gold_to_redshift
    )
