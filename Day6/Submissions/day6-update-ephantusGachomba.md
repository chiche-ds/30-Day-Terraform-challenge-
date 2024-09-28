
---

### **What is Terraform State?**
Terraform state records information about the infrastructure that Terraform creates. This information is stored in a Terraform state file.

### **Shared Storage for State Files**
Storing Terraform state in version control is not recommended for the following reasons:

1. **Manual Error**: It’s easy to forget to pull down the latest changes from version control, leading to potential conflicts or outdated states.
2. **Locking**: Version control systems do not provide any form of locking to prevent two team members from running `terraform apply` on the same state file simultaneously.
3. **Secrets**: All data in Terraform state files is stored in plain text, which could expose sensitive information.

---

### **`variables.tf`**

```hcl
variable "bucket_name" {
  description = "terraform-s3bucket-efantus"
  type        = string
}

variable "table_name" {
  description = "DynamoDBtableTerraformEfantus"
  type        = string
}
```

### **`main.tf`**

```hcl
terraform {
  required_version = ">= 1.0.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = var.bucket_name

  # This is only here so we can destroy the bucket as part of automated tests.
  # You should not copy this for production usage.
  force_destroy = true
}

# Enable versioning to track the full revision history of your state files
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
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}


![locked_status](https://github.com/user-attachments/assets/87a9ac7a-d2c1-47f4-bfb8-3a2ab6ad378f)
![locked_status](https://github.com/user-attachments/assets/a5db2a82-3899-4c67-9a15-08abbc9857b1)
![S3_dynamodb](https://github.com/user-attachments/assets/6d6c66c4-0fea-4806-9e32-3799e12d317f)
![locked_status](https://github.com/user-attachments/assets/5951e06f-46f4-4070-8728-548db8a491e0)

terraform {
  backend "s3" {
    # Replace this with your bucket name!
    bucket         = "terraformephantusdemo"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-2"
    # Replace this with your DynamoDB table name!
    dynamodb_table = "terraformdynamodbdemo"
    encrypt        = true
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

---
