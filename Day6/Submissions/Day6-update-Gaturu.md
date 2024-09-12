# Day 6: Understanding Terraform State

## Participant Details
- **Name:**: Duncan Gaturu
- **Task Completed:**: Understanding Terraform State
- **Date and Time:** : 2024-09-05 at 7:00 pm
  
### Remote State Management with Amazon S3
#### main.tf

```hcl
# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# create an S3 bucket by using the aws_s3_bucket resource:

resource "aws_s3_bucket" "terraform_state" {
  bucket = "gaturu-terraform-up-and-running-state"
  # Prevent accidental deletion of this S3 bucket
  lifecycle {
    prevent_destroy = true
  }
}

#add several extra layers of protection to this S3 bucket.
# Enable versioning so you can see the full revision history of your
# state files
resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

#Encryption configuration
# Enable server-side encryption by default
resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.terraform_state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

#Preventing public access to the S3 bucket
# Explicitly block all public access to the S3 bucket
resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

#Creating a dynamo Db for our state lock
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-up-and-running-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}

#configure Terraform to store the state in your S3 bucket 
terraform {
  backend "s3" {
    # Replace this with your bucket name!
    bucket         = "terraform-up-and-running-state"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-2"
    # Replace this with your DynamoDB table name!
    dynamodb_table = "terraform-up-and-running-locks"
    encrypt        = true
  }
}
```


