# Day 6: Understanding Terraform State

## Participant Details
- **Name:** Ajibola Mubarak
- **Task Completed:** 
  - I have completed Chapter 3 (Pages 81-113) 
    - Sections:
      - "What is Terraform State?"
      - "Shared Storage for State Files"
      - "Managing State Across Teams"
- **Videos Watched:**
  - **"Benefits of Terraform State"** (Video 47)
  - **"Managing Terraform State"** (Video 48)
  - **"Remote State Storage"** (Video 49)
  - **"State Locking and Backend Authentication"** (Video 50)

### Configured remote state storage using S3 and locked the state using DynamoDB

#### main.tf

```hcl
terraform {
  backend "s3" {
    bucket         = "dexter-s3-bucket" 
    key            = "terraform/state.tfstate"
    region         = "us-west-2"
    encrypt        = true
  }
}

# Define the provider
provider "aws" {
  region = "us-west-2" # Replace with your preferred region
}

# Create an S3 bucket
resource "aws_s3_bucket" "my_bucket" {
  bucket = "dexter504-s3-bucket" 
  
  # Tag the bucket
  tags = {
    Name        = "MyS3Bucket"
    Environment = "Dev"
  }
}

# Manage versioning as a separate resource
resource "aws_s3_bucket_versioning" "my_bucket_versioning" {
  bucket = aws_s3_bucket.my_bucket.bucket

  versioning_configuration {
    status = "Enabled"
  }
}
