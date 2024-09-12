## Tasks Completed

## 1. **Reading**
- I have Completed Chapter 3 (Pages 81-113)
- Sections: "State File Isolation", "Isolation via Workspaces", "Isolation via Files Layout", and "The Remote State Source".
   - I Understand the two primary methods of state isolation and how to manage state across different environments.

## 2. **Videos**
     - Video 51: "Terraform remote state - Enhanced Backend"
     - Video 52: "Terraform state migration"
     - Video 53: "Terraform Backend configuration"
     - Video 54: "State Locking Best Practices"
     - Video 55: "Terraform State in a Team Environment"

## Configure your environment variables:

```
export AWS_ACCESS_KEY_ID=(your access key id)
export AWS_SECRET_ACCESS_KEY=(your secret access key)
```
## Deploy the code:
```hcl
terraform init
terraform apply
```
## Create a new workspace: Stage

```
terraform workspace new Stage
```

## Create a new workspace: Production

```
terraform workspace new Production
```

## Then switch back to the default workspace:

```
terraform workspace switch default
```





```hcl

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-up-and-running-state-Lobuin"
  
  # Prevent accidental deletion of this S3 bucket
  lifecycle {
    prevent_destroy = false
  }
}

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
  name         = "terraform-up-and-running-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}
```
