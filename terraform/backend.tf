terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "teachable/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock-table"
  }
}
