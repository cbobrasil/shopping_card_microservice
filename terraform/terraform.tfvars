# S3 Configuration
s3_bucket_name    = "s3_techable_bucket"
bronze_layer_path = "bronze/purchase_orders.parquet"

# Kafka Configuration
kafka_conn_id     = "kafka_connector"
kafka_topic       = "purchase_orders"

# AWS Connection
aws_conn_id       = "aws_techable"

# DynamoDB Configuration
dynamodb_table_name = "purchase_orders"

# Redshift Configuration
redshift_cluster_identifier = "redshift-cluster-techable"
redshift_database_name      = "analytics_db"
redshift_master_username    = "admin"
redshift_master_password    = "your_secure_password"
redshift_node_type          = "dc2.large"
redshift_number_of_nodes    = 2

# Monitoring and Alerts
alert_email       = "data_engineer@teachable.com"
cloudwatch_metric_namespace = "TeachableMetrics"

# Schema Validation Lambda Configuration
expected_schema = jsonencode({
  buyer_id                = "string",
  product_id              = "string",
  number_of_installments  = "int",
  total_amount            = "float",
  purchase_date           = "string"
})
schema_validation_lambda_name = "validate_s3_parquet_schema"

# General
region = "us-east-1"
