# Day 8: Reusing Infrastructure with Modules

## Participant Details
- **Name:** Njoku Ujunwa Sophia
- **Task Completed:** Terraform module for EC2 instance
- **Date and Time:** 9/03/2024 10:38 AM

## main.tf
```hcl
module "ec2_instance" {
  source = "./modules/ec2-instance"
  instance_type  = var.instance_type
  region = var.region
}

variable "region" {
  description = "The AWS region to deploy the instance in"
  default      = "us-east-1"
}

variable "instance_type" {
  description = "The EC2 instance type"
  default     = "t2.micro"
}
```

## modules.tf
```hcl
# ./modules/ec2-instance/main.tf

provider "aws" {
  region = var.region
}

data "aws_ami" "latest" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["amazon"]
}

variable "region" {}
variable "instance_type" {}

resource "aws_instance" "this" {
  ami           = data.aws_ami.latest.id 
  instance_type = var.instance_type
  tags = {
    Name = "testing"
  }
}
