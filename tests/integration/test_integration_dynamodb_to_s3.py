import boto3
from moto import mock_dynamodb, mock_s3
import pytest
import json
from lambda_function import lambda_handler  # Replace with the actual name of your Lambda function file

# Constants
DYNAMODB_TABLE_NAME = "purchase_orders"
S3_BUCKET_NAME = "bronze-layer"
BRONZE_FOLDER = "bronze_folder"

@pytest.fixture
def setup_dynamodb_and_s3():
    """Set up mocked DynamoDB and S3 resources."""
    # Mock DynamoDB
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName=DYNAMODB_TABLE_NAME,
            KeySchema=[{"AttributeName": "buyer_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "buyer_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
            StreamSpecification={"StreamEnabled": True, "StreamViewType": "NEW_IMAGE"}
        )
        # Insert sample data into DynamoDB
        table.put_item(
            Item={
                "buyer_id": "123",
                "product_id": "456",
                "number_of_installments": 3,
                "total_amount": 150.75,
                "purchase_date": "2024-01-01"
            }
        )

        # Mock S3
        with mock_s3():
            s3 = boto3.client("s3", region_name="us-east-1")
            s3.create_bucket(Bucket=S3_BUCKET_NAME)

            yield {"dynamodb": dynamodb, "s3": s3}


def generate_dynamodb_stream_event():
    """Generate a mock DynamoDB Stream event."""
    return {
        "Records": [
            {
                "eventName": "INSERT",
                "dynamodb": {
                    "NewImage": {
                        "buyer_id": {"S": "123"},
                        "product_id": {"S": "456"},
                        "number_of_installments": {"N": "3"},
                        "total_amount": {"N": "150.75"},
                        "purchase_date": {"S": "2024-01-01"}
                    }
                }
            }
        ]
    }


def test_dynamodb_to_s3_integration(setup_dynamodb_and_s3):
    """Test DynamoDB to S3 integration."""
    # Generate the DynamoDB Stream event
    event = generate_dynamodb_stream_event()

    # Call the Lambda handler
    response = lambda_handler(event, None)
    assert response["statusCode"] == 200

    # Verify the data in S3
    s3 = setup_dynamodb_and_s3["s3"]
    response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=BRONZE_FOLDER)
    assert "Contents" in response, "No files found in S3"
    assert len(response["Contents"]) > 0, "No files written to S3"

    # Check the content of the uploaded file
    file_key = response["Contents"][0]["Key"]
    file_object = s3.get_object(Bucket=S3_BUCKET_NAME, Key=file_key)
    file_content = json.loads(file_object["Body"].read().decode("utf-8"))

    # Validate the data matches the DynamoDB item
    assert len(file_content) == 1
    assert file_content[0]["buyer_id"] == "123"
    assert file_content[0]["product_id"] == "456"
    assert file_content[0]["number_of_installments"] == 3
    assert file_content[0]["total_amount"] == 150.75
    assert file_content[0]["purchase_date"] == "2024-01-01"
