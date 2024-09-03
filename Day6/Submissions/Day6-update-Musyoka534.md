# Day 6: Understanding Terraform State

## Participant Details
- **Name:** Musyoka Kilonzo
- **Task Completed:** Completed reading chapter 3 of the book,sections on Terraform state.Watched videos 47,48,49 and 50.Configured Terraform remote state using AWS s3 Bucket.
- **Date and Time:** 8/27/2024 12:00PM

 
# Terraform Code - Secure Terraform State Management with AWS S3 and DynamoDB.

**Code explanantion:** This code sets up a secure Terraform backend on AWS using S3 for state storage with versioning and encryption enabled.I have also leveraged DynamoDB for state locking to prevent concurrent modifications. It also includes lifecycle rules to prevent accidental deletion and blocks public access to the S3 bucket.
### main.tf

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Create s3 bucket for storing our state file
resource "aws_s3_bucket" "terraform_state" {
 bucket = "musyokaterraforms3"
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
```
### backend.tf
```hcl
terraform {
 backend "s3" {
 # Replace this with your bucket name!
 bucket = "musyokaterraforms3"
 key = "global/s3/terraform.tfstate"
 region = "us-east-1"
 # Replace this with your DynamoDB table name!
 dynamodb_table = "terraform-up-and-running-locks"
 encrypt = true
 }
}

```
### Terraform state inspection.

```hcl
{
  "version": 3,
  "terraform_version": "1.9.4",
  "backend": {
    "type": "s3",
    "config": {
      "access_key": null,
      "acl": null,
      "allowed_account_ids": null,
      "assume_role": null,
      "assume_role_duration_seconds": null,
      "assume_role_policy": null,
      "assume_role_policy_arns": null,
      "assume_role_tags": null,
      "assume_role_transitive_tag_keys": null,
      "assume_role_with_web_identity": null,
      "bucket": "musyokaterraforms3",
      "custom_ca_bundle": null,
      "dynamodb_endpoint": null,
      "dynamodb_table": "terraform-up-and-running-locks",
      "ec2_metadata_service_endpoint": null,
      "ec2_metadata_service_endpoint_mode": null,
      "encrypt": true,
      "endpoint": null,
      "endpoints": null,
      "external_id": null,
      "forbidden_account_ids": null,
      "force_path_style": null,
      "http_proxy": null,
      "https_proxy": null,
      "iam_endpoint": null,
      "insecure": null,
      "key": "global/s3/terraform.tfstate",
      "kms_key_id": null,
      "max_retries": null,
      "no_proxy": null,
      "profile": null,
      "region": "us-east-1",
      "retry_mode": null,
      "role_arn": null,
      "secret_key": null,
      "session_name": null,
      "shared_config_files": null,
      "shared_credentials_file": null,
      "shared_credentials_files": null,
      "skip_credentials_validation": null,
      "skip_metadata_api_check": null,
      "skip_region_validation": null,
      "skip_requesting_account_id": null,
      "skip_s3_checksum": null,
      "sse_customer_key": null,
      "sts_endpoint": null,
      "sts_region": null,
      "token": null,
      "use_dualstack_endpoint": null,
      "use_fips_endpoint": null,
      "use_path_style": null,
      "workspace_key_prefix": null
    },
    "hash": 788032418
  }
}
```




