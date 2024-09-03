# Day 6: Understanding Terraform State

## Participant Details
- **Name:** NGWA DIEUDONNE LOBUIN
- **Task Completed:** I have Completed Chapter 3 (Pages 81-113) Sections "What is Terraform State?", "Shared Storage for State Files", and "Managing State Across Teams".
- I have watched **"Benefits of Terraform State"** (Video 47)
- I have watched **"Managing Terraform State"** (Video 48)
- I have watched **"Remote State Storage"** (Video 49)
- I have watched **"State Locking and Backend Authentication"** (Video 50)



  
- **Date and Time:** 09/02/2024 10:30 AM

 
# Terraform Code to Secure Terraform State Management with S3 and DynamoDB

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
# Architecture Diagram for Terraform State Management with AWS S3 and DynamoDB
[Terraform State Management with AWS S3 and DynamoD](https://deyobucket.s3.amazonaws.com/Diagram+of+a+cluster+of+Web+Servers++with+Auto-scaling+Group.png)
