Day 5: Understanding Terraform State
Name: Udeh Samuel Chibuike
Task Completed: Create a remote storage
Date and Time: 12/22/2024 2:05pm

provider "aws" {
  region = "us-east-1"  # Adjust as needed
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "samley-bucket"  # Ensure this name is unique across all of AWS
  acl    = "private"         # Set the ACL for the bucket

  versioning {
    enabled = true  # Enable versioning
  }

  # Enable server-side encryption
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"  # Use S3-managed keys for encryption
      }
    }
  }


  lifecycle {
    prevent_destroy = true  # Prevent accidental deletion
  }
}

# Block public access settings for the bucket
resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy      = true
  restrict_public_buckets  = true
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "state-locks"
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

terraform {
  backend "s3" {
    bucket         = "samley-bucket"  
    key            = "global/s3/terraform.tfstate"  
    region         = "us-east-1"  
    dynamodb_table = "state-locks"  
    encrypt        = true  
  }
}