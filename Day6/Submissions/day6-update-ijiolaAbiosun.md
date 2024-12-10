
# Terraform State Management Configuration

## 1. Configure the AWS Provider
```hcl
provider "aws" {
  region = "us-east-1"
}
```

## 2. Create an S3 Bucket for Terraform State Storage
```hcl
resource "aws_s3_bucket" "statefile_bucket" {
  bucket = var.aws_s3_bucket_name

  versioning {
    enabled = true
  }

  tags = {
    Name        = "TerraformStateBucket"
    Environment = "Testing"
  }
}
```

## 3. Define S3 Bucket ACL
```hcl
resource "aws_s3_bucket_acl" "statefile_bucket_acl" {
  bucket = aws_s3_bucket.statefile_bucket.id
  acl    = "private"
}
```

## 4. Define Server-Side Encryption for S3 Bucket
```hcl
resource "aws_s3_bucket_server_side_encryption_configuration" "statefile_bucket_encryption" {
  bucket = aws_s3_bucket.statefile_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```

## 5. Create a DynamoDB Table for State File Locking
```hcl
resource "aws_dynamodb_table" "statefile_locks" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S" # "S" means String type
  }

  tags = {
    Name        = "TerraformStateLockTable"
    Environment = "Testing"
  }
}
```

## 6. Configure the Terraform Backend
```hcl
terraform {
  backend "s3" {
    bucket         = "my-s3-bucket-state-3848384839"
    key            = "terraform/statefile.tfstate" # Path to the state file
    region         = "us-east-1"
    dynamodb_table = "statefile-locks"
    encrypt        = true
  }
}
```

---


