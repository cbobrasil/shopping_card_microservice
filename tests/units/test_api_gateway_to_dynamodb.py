import json
import boto3
import os

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE')  # Environment variable for table name
table = dynamodb.Table(table_name)

def validate_payload(payload):
    """Validate the incoming payload structure."""
    required_fields = ["buyer_id", "product_id", "number_of_installments", "total_amount", "purchase_date"]
    for field in required_fields:
        if field not in payload:
            raise ValueError(f"Missing required field: {field}")
    return True

def lambda_handler(event, context):
    """Lambda function handler for API Gateway."""
    try:
        # Parse the request body
        body = json.loads(event.get('body', '{}'))

        # Validate the payload
        validate_payload(body)

        # Save the data to DynamoDB
        table.put_item(Item={
            "buyer_id": str(body["buyer_id"]),
            "product_id": str(body["product_id"]),
            "number_of_installments": int(body["number_of_installments"]),
            "total_amount": float(body["total_amount"]),
            "purchase_date": body["purchase_date"]
        })

        # Return success response
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Data saved successfully"})
        }
    except ValueError as e:
        # Return validation error response
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }
    except Exception as e:
        # Return general error response
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }
