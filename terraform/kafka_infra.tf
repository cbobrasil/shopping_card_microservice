resource "kafka_topic" "purchase_orders" {
  name               = var.kafka_topic
  partitions         = 3
  replication_factor = 2
}
