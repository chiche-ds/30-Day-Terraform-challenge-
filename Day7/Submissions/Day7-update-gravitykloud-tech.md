## Participant Details
- **Name:** gus
- **Task Completed:** 
- **Date and Time:** 9/3/2024 15:30 PM

# Terraform Code - Secure Terraform State Management with S3 and DynamoDB
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  profile = "Dev-Prof"

  region = "us-west-1"
}

resource "aws_instance" "example" {
ami = "ami-0e64c0b934d72ced5"
instance_type = "t2.micro"
}
#Configured a backend for this AMI Instance using the S3 bucket and DynamoDB table
terraform {
backend "s3" {
# Replace this with your bucket name!
bucket = "terraform-up-and-running-state"
key = "workspaces-example/terraform.tfstate"
region = "us-west-1"
# Replace this with your DynamoDB table name!
dynamodb_table = "terraform-up-and-running-locks"
encrypt = true
}
}
```
# Workspaces: Set up isolated environments for development, using Workspaces.
## Isolation via Workspaces,Terraform workspaces allow you to store your Terraform state in multiple, separate,named workspaces.
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
Configure the AWS Provider
provider "aws" {
  profile = "Dev-Prof"

  region = "us-west-1"
}

resource "aws_instance" "example" {
ami = "ami-0e64c0b934d72ced5"
instance_type = "t2.micro"
}
```
