### Name: Ejibode Ibraheem
### Task: Day 6: Understanding Terraform State
### Date: 07/12/2024
### Time: 9:20 PM

### Understanding Terraform State and State Locking

i. I learned about state files; S3 standard backend and remote enhanced backend aside from the local backend which is terraform default.

ii. I also learned about state locking using AWS Dynamo DB and HTTP standard locking 

iii. I Learned about enabling versioning and encryption on AWS S3 bucket.

iv  I made a post on Linkedn 
```
provider "aws" {
region = "us-east-2"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "linsmed-s3-bucket-for-terraform-project"

  # prevent accidental deletion of this s3 bucket
  lifecycle {
    prevent_destroy = true
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
 bucket = aws_s3_bucket.terraform_state.id
 block_public_acls = true
 block_public_policy = true
 ignore_public_acls = true
 restrict_public_buckets = true
}

resource "aws_dynamodb_table" "terraform_locks" {
 name = "ejibode-dynamodb"
 billing_mode = "PAY_PER_REQUEST"
 hash_key = "LockID"
 attribute {
 name = "LockID"
 type = "S"
 }
}

terraform {
 backend "s3" {
 
 bucket = "linsmed-s3-bucket-for-terraform-project"
 key = "global/s3/terraform.tfstate"
 region = "us-east-2"
 # Replace this with your DynamoDB table name!
 dynamodb_table = "ejibode-dynamodb"
 encrypt = true
 }
}
```