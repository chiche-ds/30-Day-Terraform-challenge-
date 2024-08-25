# Day 7: Understanding Terraform State

## Participant Details
- **Name:** Kevin Tuei
- **Task Completed:** : Workspace Layout and File Layouts
- **Date and Time:** 2024-08-24 7:36pm


### Practice using Workspace Layout to manage terraform State
#### main.tf
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-up-and-running-state-tuei"
  # Prevent accidental deletion of this S3 bucket
  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable server-side encryption by default
resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.terraform_state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Explicitly block all public access to the S3 bucket
resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-up-and-running-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}
```

#### backend.hcl
```hcl
# backend.hcl
bucket = "terraform-up-and-running-state-tuei"
region = "us-east-1"
dynamodb_table = "terraform-up-and-running-locks"
encrypt = true
```


My updated Architecture Diagram with a State file in a Bucket

![AWS VPC Architecture](https://tuei-aws-diagrams.s3.amazonaws.com/StateFile.png)