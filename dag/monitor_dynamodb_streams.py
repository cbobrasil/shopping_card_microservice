from airflow import DAG
from airflow.providers.amazon.aws.sensors.dynamodb_stream import DynamoDBStreamSensor
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta

# DAG Configuration
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'monitor_dynamodb_streams',
    default_args=default_args,
    description='Monitor DynamoDB Streams and trigger the next DAG',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Start Dummy Task
    start_monitoring = DummyOperator(
        task_id='start_monitoring'
    )

    # DynamoDB Stream Sensor
    monitor_streams = DynamoDBStreamSensor(
        task_id='monitor_dynamodb_streams',
        table_name='purchase_orders',  
        aws_conn_id='aws_default',
        stream_view_type='NEW_IMAGE',  
        poke_interval=30,  
        timeout=3600 
    )

    # Trigger Next DAG (DynamoDB to Bronze)
    trigger_next_dag = TriggerDagRunOperator(
        task_id='trigger_dynamodb_to_bronze_dag',
        trigger_dag_id='dynamodb_to_bronze_dag', 
        wait_for_completion=False,
    )

    # Define DAG Flow
    start_monitoring >> monitor_streams >> trigger_next_dag
