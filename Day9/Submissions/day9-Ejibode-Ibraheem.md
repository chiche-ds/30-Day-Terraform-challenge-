# Day 9: Continuing Reuse of Infrastructure with Modules

## Participant Details
- **Name:** Ejibode Ibraheem A
- **Task Completed:**  Watched videos on scope,public registry and versioning from the udemy videos. I also learnt and practiced multiple environments (dev, staging, production)
- **Date and Time:** 14/12/2024 12:25 PM

### This is the `main.tf` with the AWS S3 bucket remote backend is configured and versioning is enabled,encryption is enabled, block public acceess and also create the Dynamo DB table for locking  
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "adaeze-terraform-bucket"
  # Prevent accidental deletion of this S3 bucket
  lifecycle {
    prevent_destroy = false 
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

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "ib-terraform-up-and-running-locks"
  billing_mode = "PAY_PER_REQUEST"

  server_side_encryption {
    enabled = true
  }
  hash_key = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}

# Create an EC2 instance
resource "aws_instance" "my-instance" {
  ami           = "ami-066784287e358dad1"
  instance_type = "t2.micro"
}

```
### This is the `output.tf` file where The ARN of the S3 bucket shows and Dynamo DB name shows as well.

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
