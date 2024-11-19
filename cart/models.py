import boto3
import os
from botocore.exceptions import ClientError

class ShoppingCart:
    def __init__(self):
        self.table_name = os.getenv("DYNAMODB_TABLE_NAME", "ShoppingCartTable")
        self.dynamodb = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION", "us-east-1"))
        self.table = self.dynamodb.Table(self.table_name)

    def add_item(self, user_id, item_id, quantity):
        try:
            self.table.update_item(
                Key={"user_id": user_id},
                UpdateExpression="SET items.#item_id = :quantity",
                ExpressionAttributeNames={"#item_id": item_id},
                ExpressionAttributeValues={":quantity": quantity},
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            raise Exception(f"Failed to add item: {e.response['Error']['Message']}")

    def remove_item(self, user_id, item_id):
        try:
            self.table.update_item(
                Key={"user_id": user_id},
                UpdateExpression="REMOVE items.#item_id",
                ExpressionAttributeNames={"#item_id": item_id},
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            raise Exception(f"Failed to remove item: {e.response['Error']['Message']}")

    def get_cart(self, user_id):
        try:
            response = self.table.get_item(Key={"user_id": user_id})
            return response.get("Item", {}).get("items", {})
        except ClientError as e:
            raise Exception(f"Failed to fetch cart: {e.response['Error']['Message']}")
