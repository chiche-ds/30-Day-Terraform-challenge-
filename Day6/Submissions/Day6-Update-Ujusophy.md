# Day 6: Understanding Terraform State

- **Name:** Njoku Ujunwa Sophia
- **Task:** Configure remote state storage using AWS S3 
- **Date and Time:** 8/30/2024 03:26 PM


## main.tf
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "tf_state_bucket" {
  bucket = "techynurse-tf-state-bucket"  

  tags = {
    Name = "tf-state-bucket"
  }
}

resource "aws_s3_bucket_versioning" "tf_state_bucket_versioning" {
  bucket = aws_s3_bucket.tf_state_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "tf_lock_table" {
  name         = "terraform-lock-table"  
  billing_mode = "PAY_PER_REQUEST"

  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name = "terraform-lock-table"
  }
}
```


## backend.tf

### N.B: This will run after the S3 and Dynamodb has been created
```hcl
terraform {
  backend "s3" {
    bucket         = "techynurse-tf-state-bucket" 
    key            = "terraform/state.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock-table"
  }
}
```
