# Day 3: Deploying Basic Infrastructure with Terraform

## Participant Details

- **Name:** Duncan Gaturu
- **Task Completed:** Deploying Basic Infrastructure with Terraform
- **Date and Time:** 2024-08-22 at 9:00 pm

## Terraform Code 

main.tf
```bash
# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance""my-first-server"
ami      "ami-0e86e20dae9224db8"
instance_type = "t3.micro"

tag = {
Name = "Web Server"
}
