import pytest
from app import app
from moto import mock_dynamodb
import boto3

@pytest.fixture
def client():
    """Provides a test client for Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_dynamo_table():
    """Sets up a mocked DynamoDB table for testing."""
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName="ShoppingCartTable",
            KeySchema=[{"AttributeName": "user_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "user_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        table.meta.client.get_waiter("table_exists").wait(TableName="ShoppingCartTable")
        yield table

def test_add_item_route(client, mock_dynamo_table):
    response = client.post(
        "/cart/add",
        json={"user_id": "user1", "item_id": "item1", "quantity": 2},
    )
    assert response.status_code == 201
    assert response.json["message"] == "Item added"

def test_remove_item_route(client, mock_dynamo_table):
    client.post("/cart/add", json={"user_id": "user1", "item_id": "item1", "quantity": 2})
    response = client.post("/cart/remove", json={"user_id": "user1", "item_id": "item1"})
    assert response.status_code == 200
    assert response.json["message"] == "Item removed"

def test_get_cart_route(client, mock_dynamo_table):
    client.post("/cart/add", json={"user_id": "user1", "item_id": "item1", "quantity": 2})
    response = client.get("/cart/", query_string={"user_id": "user1"})
    assert response.status_code == 200
    assert response.json["cart"]["item1"] == 2
