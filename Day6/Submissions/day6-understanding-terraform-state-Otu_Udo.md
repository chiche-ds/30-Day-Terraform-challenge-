# I really enjoyed lerning how to manage terraform states using the remote backend . using encryption and ACL for security, version control to easily revert to the previous state incase of problems. Last but not the least using Separate Environments with Workspaces: Keep dev, staging, and production states isolated to avoid conflicts.




provider "aws" {
 region = "us-east-1"
}

resource "aws_s3_bucket" "terraform_state" {
 bucket = "otu-bucket-state"
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
 name = "state-locks"
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
 bucket = "otu-bucket-state"
 key = "global/s3/terraform.tfstate"
 region = "us-east-1"
 # Replace this with your DynamoDB table name!
 dynamodb_table = "state-locks"
 encrypt = true
 }
}

output "s3_bucket_arn" {
 value = aws_s3_bucket.terraform_state.arn
 description = "The ARN of the S3 bucket"
}
output "dynamodb_table_name" {
 value = aws_dynamodb_table.terraform_locks.name
 description = "The name of the DynamoDB table"
}

