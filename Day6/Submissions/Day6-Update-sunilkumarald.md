**Day6:
Understanding Terraform State**
**Participant Details**
**Name:** 
Sunil Kumar
**Task Completed:** 
Read Chapter 3 (Pages 81-113), Sections: "What is Terraform State?", "Shared Storage for State Files", and "Managing State Across Teams" from the book Terraform Up and Running by Yevgeniy Brickman.
**Hands-on Activity completed:**
(i)Deployed infrastructure and inspect the Terraform state file.
(ii)Configure remote state storage using AWS S3 or another cloud provider.
**Date and Time:** 04-09-2024 at 07:23 am IST

**main.tf **
#provider block
provider "aws" {
region = "ap-south-1"
}
**#s3 bucket creation**
resource "aws_s3_bucket" "terraform_state" {
bucket = "terraform-up-and-running-state-digibodh2"
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
**#Dynamodb table**
resource "aws_dynamodb_table" "terraform_locks" {
name = "terraform-up-and-running-locks-2"
billing_mode = "PAY_PER_REQUEST"
hash_key = "LockID"
attribute {
name = "LockID"
type = "S"
}
}

/*terraform {
backend "s3" {
# Replace this with your bucket name!
bucket = "terraform-up-and-running-state-digibodh"
//key = "global/s3/terraform.tfstate"
key = "workspaces-example/terraform.tfstate"
region = "ap-south-1"
# Replace this with your DynamoDB table name!
dynamodb_table = "terraform-up-and-running-locks"
encrypt = true
}
}*/
output "s3_bucket_arn" {
value = aws_s3_bucket.terraform_state.arn
description = "The ARN of the S3 bucket"
}
output "dynamodb_table_name" {
value = aws_dynamodb_table.terraform_locks.name
description = "The name of the DynamoDB table"
}
**#statefile isolation**
resource "aws_instance" "exampleday7" {
ami = "ami-0xxx"
instance_type = "t2.micro"
}
