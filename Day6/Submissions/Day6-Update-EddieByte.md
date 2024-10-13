# Day 6: Understanding Terraform State

## Participant Details
- **Name:** Eddie Chem
- **Task Completed:** Began learning about Terraform State, and the vital role it plays in "mapping out the state" of our infrastructure thus adding more efficiency to the process of resource provisioning. Also learned about the pros and cons of storing Terraform State files in both remote and local backends. Learned how to safeguard Terraform statefiles and Terraform Locks.
- **Date and Time:** 8/23/2024 11:01 PM

 
# Terraform Code - Secure Terraform State Management with S3 and DynamoDB

**Code Summary:** This code sets up a secure Terraform backend on AWS using S3 for state storage with versioning and encryption, while also leveraging DynamoDB for state locking to prevent concurrent modifications. It includes lifecycle rules to prevent accidental deletion and blocks public access to the S3 bucket.

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "path/to/terraform.tfstate"
    region         = "us-east-2"
    encrypt        = true
    dynamodb_table = "terraform-state-locks"
  }
}

provider "aws" {
  region = "us-east-2"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "my-terraform-state-bucket"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

output "s3_bucket_arn" {
  value       = aws_s3_bucket.terraform_state.arn
  description = "The ARN of the S3 bucket"
}

output "dynamodb_table_name" {
  value       = aws_dynamodb_table.terraform_locks.name
  description = "The name of the DynamoDB table"
}
```
# Architecture Diagram: Terraform State Management with AWS S3 and DynamoDB
![Architecture Diagram](https://drive.google.com/uc?export=view&id=1PeGH-21DHUo0nsHO6VJLIN78GpPi-Qyo)
