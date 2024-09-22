# Day 7: Understanding Terraform State

## Participant Details
- **Name:** Patrick Odhiambo
- **Task Completed:** : Workspace Layout and File Layouts
- **Date and Time:** 2024-9-13 10:36pm

## Terraform Code

# backend.tf

terraform {
  backend "s3" {
    bucket         = "backendpat"                        # The S3 bucket name
    key            = "global/mystatefile/terraform.tfstate" # Path for storing state file
    region         = "us-east-1"                          # The AWS region
    encrypt        = true                                 # Enable server-side encryption
    dynamodb_table = "my-terraform-locky-table"           # Replace with the actual DynamoDB table name  
  }

  required_version = ">= 1.0.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# s3.tf 

resource "aws_s3_bucket" "backendpat" {
  bucket = var.bucket_name

  # This is only here so we can destroy the bucket as part of automated tests.
  # You should not copy this for production usage
  force_destroy = true
}

# Enable versioning so you can see the full revision history of your state files
resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.backendpat.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable server-side encryption by default
resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.backendpat.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Explicitly block all public access to the S3 bucket
resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket                  = aws_s3_bucket.backendpat.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


# dymanodb.tf

resource "aws_dynamodb_table" "my-terraform-locky-table" {
  name           = "my-terraform-locky-table"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

# outputs.tf

output "s3_bucket_arn" {
  value       = aws_s3_bucket.backendpato.arn
  description = "The ARN of the S3 bucket"
}

output "dynamodb_table_name" {
  value       = aws_dynamodb_table.my-terraform-locky1-table
  description = "The name of the DynamoDB table"
}

# variables.tf

variable "bucket_name" {
  description = "The name of the S3 bucket to store the Terraform state"
  type        = string
}

