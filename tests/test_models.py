import pytest
from moto import mock_dynamodb
import boto3
from cart.models import ShoppingCart

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

def test_add_item(mock_dynamo_table):
    cart = ShoppingCart()
    cart.add_item(user_id="user1", item_id="item1", quantity=2)

    response = mock_dynamo_table.get_item(Key={"user_id": "user1"})
    items = response["Item"]["items"]
    assert items["item1"] == 2

def test_remove_item(mock_dynamo_table):
    cart = ShoppingCart()
    cart.add_item(user_id="user1", item_id="item1", quantity=2)
    cart.remove_item(user_id="user1", item_id="item1")

    response = mock_dynamo_table.get_item(Key={"user_id": "user1"})
    assert "items" not in response["Item"]

def test_get_cart(mock_dynamo_table):
    cart = ShoppingCart()
    cart.add_item(user_id="user1", item_id="item1", quantity=2)

    items = cart.get_cart(user_id="user1")
    assert items["item1"] == 2
