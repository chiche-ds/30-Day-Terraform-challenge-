# Day 2: Deploying basic infrastuctuter with Terraform

## Participant Details

- **Name:** gus
- **Task Completed:** Deploying a Single Server, Create new update file. Embed code

- **Date and Time:** 08-21-2024 at 10:22 am

provider "aws" {
  region = "us-west-1"
  profile ="dev-profile"
}

resource "aws_instance" "Terraform_Instance_AMI" {
  ami           = "ami-0e64c0b934d72ced5"
  instance_type = "t2.micro"

  tags = {
    Name = "Terraform Instance AMI"
  }
}
