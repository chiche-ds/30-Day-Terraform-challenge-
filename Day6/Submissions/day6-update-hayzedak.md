# Day 6: Understanding Terraform State

- **Name:** Akintola AbdulAzeez 
- **Task:** Configure remote state storage using AWS S3 
- **Date and Time:** 11/10/2024 9:00 PM

main.tf
# Define the provider
```
provider "aws" {
  region = "us-west-2" ferred region
}

# Create an S3 bucket
resource "aws_s3_bucket" "my_bucket" {
  bucket = "maryjaneer-s3-bucket" 
  # Set access control (public-read, private, etc.)

  
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
    status = "Enabled"
  }
}
```

backend.tf 
```
terraform {
  backend "s3" {
    bucket         = "maryjaneer-s3-bucket" 
    key            = "terraform/state.tfstate"
    region         = "us-west-2"
    encrypt        = true
  }
}
```