# Day 6: Understanding Terraform State

## Participant Details

- **Name:** Maryjane Enechukwu
- **Task Completed:** Completed the course modules from 47,48,49,50 , finished the section of the book and i wrote a blog about terraform state practices
- **Date and Time:** 14/10/2024 1:10 PM



## backend.tf
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

## main.tf
# Define the provider

```
provider "aws" {
  region = "us-west-2" # Replace with your preferred region
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
    status = "Enabled"
  }
}
```