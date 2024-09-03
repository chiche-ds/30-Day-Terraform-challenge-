# Day 6: Understanding Terraform State

## Participant Details
- **Name:** BOROHOUL Soguelni Malachie
- **Task Completed:** I completed Chapter 3 and the videos, and I now understand the importance of state and the best practices for managing it.
- **Date and Time:** 8/26/2024 08:30 PM



This code creates an S3 bucket, which serves as a remote state storage solution. It helps resolve various issues discussed, such as manual errors, state locking, and secret management. I followed the Isolation via File Layout approach to organize my code effectively

#globale/s3/main.tf
```hcl
provider "aws" {
  region = "us-east-2"
}



# Create an S3 bucket for Terraform state storage
resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-bsm-my-state"
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

# Create a DynamoDB table for Terraform state locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-up-and-running-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

# Terraform backend configuration using the created S3 bucket and DynamoDB table
terraform {
  backend "s3" {
    bucket         = "terraform-bsm-my-state" # Use the bucket we created
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "terraform-up-and-running-locks"
    encrypt        = true
  }
}


```

#globale/s3/outputs.tf
```hcl
output "s3_bucket_arn" {
  value       = aws_s3_bucket.terraform_state.arn
  description = "The ARN of the S3 bucket"
}
output "dynamodb_table_name" {
  value       = aws_dynamodb_table.terraform_locks.name
  description = "The name of the DynamoDB table"
}

```

![Architecture Diagram](https://asset.cloudinary.com/dshli1qgh/93d797c4a1ec8b73c7dc4cbc2bb7d20e)