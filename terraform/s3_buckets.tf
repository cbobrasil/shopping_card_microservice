resource "aws_s3_bucket" "bronze" {
  bucket = var.s3_bucket_name
  versioning {
    enabled = true
  }
  lifecycle_rule {
    id      = "archive"
    enabled = true
    transition {
      days          = 30
      storage_class = "GLACIER"
    }
  }
}
