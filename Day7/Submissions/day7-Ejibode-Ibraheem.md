### Name: Ejibode Ibraheem Adewale
### Task: Day 7: Understanding Terraform State Part 2
### Date: 11/12/2024
### Time: 02:04am

### Understanding Terraform State Part 2

i. I learned about migrating state files from local backend to S3 backend or Remote Enhanced backend.

ii. I also learned about locking files and also applying your terraform in the "terraform cloud" user interface and having it work on your cli

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