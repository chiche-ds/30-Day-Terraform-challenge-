# Day 6: Understanding Terraform State

## Participant Details

- **Name:** Vijayaraghavan Vashudevan
- **Task Completed:** Learnt - Understand how Terraform state works, its significance in infrastructure as code, and how to manage the state effectively in a team environment.
- **Date and Time:** 28-08-2024 at 07:23 am IST

### main.tf
```bash
# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# s3 bucket creation with lifecycle
resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-up-and-running-state-vj"
  # Prevent accidental deletion of this S3 bucket
  lifecycle {
    prevent_destroy = true
  }
}

# Enable versioning so you can see the full revision history of your state files
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

#creation of dynamodb table
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-up-and-running-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
} 

#terraform-state file configuration
terraform {
 backend "s3" {
    # Replace this with your bucket name!
    bucket = "terraform-up-and-running-state-vj"       
    key  = "global/s3/terraform.tfstate"           
    region  = "us-east-2"        

    # Replace this with your DynamoDB table name!
    dynamodb_table = "terraform-up-and-running-locks"
    encrypt = true        
  }
 }
```
### terraform.tf
```bash
terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.1.0"
    }
  }
}
```
### output.tf
```bash
output "s3_bucket_arn" {
  value = aws_s3_bucket.terraform_state.arn       
  description = "The ARN of the S3 bucket"
 }
 output "dynamodb_table_name" {
  value = aws_dynamodb_table.terraform_locks.name      
  description = "The name of the DynamoDB table"
 }
```