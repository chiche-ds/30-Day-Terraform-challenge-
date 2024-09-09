# Day 6: Understanding Terraform State

## Participant Details
- **Name:** Franklin Afolabi
- **Task Completed:** Learnt about Terraform states, how important statefiles are, and how to configure remote backend.
- **Date and Time:** August 31 12:34 PM

## Terraform Code

```
terraform {
  backend "s3" {
    bucket = "tf-frankfolabi"
    key = "global/s3/terraform.tfstate"
    region = "us-east-2"

    dynamodb_table = "tf-locks"
    encrypt = true
  }

}

provider "aws" {
    region = "us-east-2"
}
// Create a unique bucket
resource "aws_s3_bucket" "tf_state" {
  bucket ="tf-frankfolabi"

  # Prevent accidental deletion of the S3 bucket
  lifecycle {
    prevent_destroy = true
  }
}

// Enable bucket versioning
resource "aws_s3_bucket_versioning" "enables" {
  bucket = aws_s3_bucket.tf_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

// Enable S3 server side encryption 
resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.tf_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

// Block public access
resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket = aws_s3_bucket.tf_state.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}


// Create DynamoDB for locking
resource "aws_dynamodb_table" "terraform_locks" {
  name = "tf-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "LockID"

  attribute {
    name = "LockID"
    type = "S"

  }
}
```