# Day 3: Deploying Basic Infrastructure with Terraform

## Participant Details

- **Name:** Teniola Adeboye
- **Task Completed:** Deploying Basic Infrastructure with Terraform
- **Date and Time:** 30/12/2024 1.27am GMT

Terraform Code

provider "aws" {
    region = "us-east-1"
}

resource "aws_instance" "web-server" {
 ami = "ami-01816d07b1128cd2d"
 instance_type = "t2.micro"
}