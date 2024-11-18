resource "aws_dynamodb_table" "purchase_orders" {
  name           = var.dynamodb_table
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "buyer_id"
  attribute {
    name = "buyer_id"
    type = "S"
  }
  stream_enabled = true
  stream_view_type = "NEW_IMAGE"
}
