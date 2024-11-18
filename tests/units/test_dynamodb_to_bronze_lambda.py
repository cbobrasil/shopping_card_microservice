import json
import boto3
import os
from datetime import datetime

# Initialize the S3 client
s3_client = boto3.client('s3')

# Environment variables for configuration
bronze_bucket = os.environ.get('BRONZE_BUCKET')  # Name of the S3 bucket
bronze_folder = os.environ.get('BRONZE_FOLDER')  # Folder in the bucket

def transform_record(record):
    """Transform a DynamoDB stream record to the desired format."""
    dynamodb_data = record['dynamodb']['NewImage']
    transformed_data = {
        "buyer_id": dynamodb_data['buyer_id']['S'],
        "product_id": dynamodb_data['product_id']['S'],
        "number_of_installments": int(dynamodb_data['number_of_installments']['N']),
        "total_amount": float(dynamodb_data['total_amount']['N']),
        "purchase_date": dynamodb_data['purchase_date']['S'],
        "processed_at": datetime.utcnow().isoformat()  # Add a processing timestamp
    }
    return transformed_data

def lambda_handler(event, context):
    """Lambda function handler for DynamoDB Streams."""
    try:
        # Collect all transformed records
        transformed_records = []

        # Process each stream record
        for record in event['Records']:
            if record['eventName'] == 'INSERT':  # Only process INSERT events
                transformed_data = transform_record(record)
                transformed_records.append(transformed_data)

        if transformed_records:
            # Generate a unique file name based on timestamp
            file_name = f"{bronze_folder}/purchase_data_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"

            # Upload the transformed data to S3
            s3_client.put_object(
                Bucket=bronze_bucket,
                Key=file_name,
                Body=json.dumps(transformed_records),
                ContentType='application/json'
            )
            print(f"Uploaded {len(transformed_records)} records to S3://{bronze_bucket}/{file_name}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Processed {len(transformed_records)} records"})
        }
    except Exception as e:
        print(f"Error processing records: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }
