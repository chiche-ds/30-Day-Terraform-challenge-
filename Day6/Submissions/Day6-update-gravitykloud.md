# Day 6: Understanding Terraform State

## Participant Details
- **Name:** gus
- **Task Completed:** 
- **Date and Time:** 8/26/2024 16:30 PM

 
# Terraform Code - Secure Terraform State Management with S3 and DynamoDB

```hcl
provider "aws" {
region = "us-west-1"
profile = "Dev-Prof"
}
resource "aws_s3_bucket" "terraform_state" {
bucket = "terraform-state-bucket-backend-shared-storage-iso"
# Prevent accidental deletion of this S3 bucket
lifecycle {
prevent_destroy = true
}
}
# Enable versioning so you can see the full revision history of your
# state files
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
bucket = aws_s3_bucket.terraform_state.id
block_public_acls = true
block_public_policy = true
ignore_public_acls = true
restrict_public_buckets = true
}
resource "aws_dynamodb_table" "terraform_locks" {
name = "terraform-up-and-running-locks"
billing_mode = "PAY_PER_REQUEST"
hash_key = "LockID"
attribute {
name = "LockID"
type = "S"
}
}
terraform {
backend "s3" {
# Replace this with your bucket name!
bucket = "terraform-state-bucket-backend-shared-storage-iso"
key = "global/s3/terraform.tfstate"
region = "us-west-1"
# Replace this with your DynamoDB table name!
dynamodb_table = "terraform-up-and-running-locks"
encrypt = true
}
}

```
