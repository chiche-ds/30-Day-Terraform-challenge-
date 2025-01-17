### Name: God'sfavour Braimah
### Task: Day 6: Understanding Terraform State
### Date: 12/9/24
### Time: 4:17pm

### Understanding Terraform State and State Locking

# Day 6: Terraform Remote State Storage with S3 and DynamoDB

Welcome to Day 6 of the Terraform 30-Day Challenge! Today, we are setting up secure remote state storage for Terraform using an S3 bucket and DynamoDB table for state locking and consistency.

---

## **Overview**
This configuration uses:
- **S3 Bucket**: To store Terraform state files securely.
- **DynamoDB Table**: To manage state locking and prevent simultaneous state updates.

---

## **Features**
1. **State Storage in S3**:
   - Versioning enabled for state file tracking.
   - Server-side encryption (AES256) for secure storage.
   - Public access explicitly blocked.
   - Prevents accidental deletion with a lifecycle rule.
2. **State Locking with DynamoDB**:
   - Ensures that only one Terraform process can modify state at a time.

---

## **Configuration Details**
### **Terraform Resources**
- **`aws_s3_bucket`**: Creates an S3 bucket for state files.
- **`aws_s3_bucket_versioning`**: Enables versioning for change tracking.
- **`aws_s3_bucket_server_side_encryption_configuration`**: Configures encryption for data protection.
- **`aws_s3_bucket_public_access_block`**: Blocks public access for enhanced security.
- **`aws_dynamodb_table`**: Sets up a DynamoDB table for state locking.

---

## **Terraform Code**
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "random_id" "bucket_suffix" {
  byte_length = 8
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-up-and-running-state-${random_id.bucket_suffix.hex}"
  # Prevent accidental deletion of this S3 bucket
}

resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

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
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-up-and-running-locks"
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
```