Participant Details

- **Name:** Maryjane Enechukwu
- **Task Completed:** 16/10/2024


# Define the provider
# set-up region for development workspace
```
hcl
provider "aws" {
  region = "us-east-1" # Replace with your preferred region
}

# region for staging
provider "aws" {
region = "us-east-2" # Replace with your preferred region
}

#region for production
provider "aws" {
 region = "us-west-1" # Replace with your preferred region
}


# # Create an S3 bucket
resource "aws_s3_bucket" "my_bucket" {
  bucket = "dexter504-s3-bucket" 
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

terraform {
  backend "s3" {
    bucket         = "dexter-s3-bucket" 
    key            = "terraform/state.tfstate"
    region         = "us-east-1" #for development workspace
    # region         = "us-east-2"
    encrypt        = true

  }
}
# Instance for development workspace (us-east-1 region)

resource "aws_instance" "development" {
 ami = "ami-0866a3c8686eaeeba"
 instance_type = "t2.micro"
}

# instance for staging workspace (us-east-2 region)
resource "aws_instance" "staging" {
 ami = "ami-0ea3c35c5c3284d82"
 instance_type = "t2.micro"

}

# instance for production workspace (us-west-1 region)
resource "aws_instance" "production" {
 ami = "ami-0da424eb883458071"
 instance_type = "t2.micro"
}
```