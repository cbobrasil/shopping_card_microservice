resource "aws_redshift_cluster" "analytics_cluster" {
  cluster_identifier = "analytics-cluster"
  node_type          = "dc2.large"
  number_of_nodes    = 2
  master_username    = "admin"
  master_password    = "password"
  publicly_accessible = false
}
