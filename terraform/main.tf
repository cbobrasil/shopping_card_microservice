provider "aws" {
  region = var.aws_region
}

module "s3" {
  source = "./s3_buckets.tf"
}

module "dynamodb" {
  source = "./dynamodb_table.tf"
}
