from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.kafka.hooks.kafka import KafkaHook
from airflow.providers.amazon.aws.hooks.dynamodb import DynamoDBHook
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from utils.utils import failure_alert, KAFKA_TOPIC , AWS_CONN_ID, KAFKA_CONN_ID
from datetime import datetime

# Function to consume messages from Kafka and write to DynamoDB
def consume_kafka_messages():
    kafka_hook = KafkaHook(kafka_conn_id=KAFKA_CONN_ID)
    messages = kafka_hook.get_conn().consume([KAFKA_TOPIC], group_id='group1')
    for message in messages:
        payload = message.value.decode('utf-8')
        # Validate payload schema here
        process_message_to_dynamodb(payload)

# Function to process the Kafka message and insert into DynamoDB
def process_message_to_dynamodb(payload):
    dynamo_hook = DynamoDBHook(aws_conn_id=AWS_CONN_ID)
    dynamo_hook.put_item(
        table_name=KAFKA_TOPIC,
        item={
            'buyer_id': payload['buyer_id'],
            'product_id': payload['product_id'],
            'total_amount': payload['total_amount'],
            'purchase_date': payload['purchase_date']
        }
    )

# DAG definition
with DAG(dag_id='kafka_to_dynamodb',
         start_date=datetime(2023, 1, 1),
         schedule_interval='@once',
         catchup=False) as dag:
    consume_messages = PythonOperator(
        task_id='consume_kafka_messages',
        python_callable=consume_kafka_messages
    )
    trigger_next_dag = TriggerDagRunOperator(
        task_id='trigger_dynamodb_to_bronze',
        trigger_dag_id='dynamodb_to_bronze'
    )

    consume_messages >> trigger_next_dag
