## Day 8: Reusing Infrastructure with Modules


## Participant's Details
**Name:** Patrick Odhiambo
**Task Completed:** Read the chapter on Terraform modules, watched the recommended videos, deployed an EC2 instance using modules, wrote a  blog and updated progress on social media
**Date and Time:** 14/9/24 at 6pm

## Terraform Code

# terraform-ec2-module

## main.tf

provider "aws" {
  region = var.region
}

resource "aws_instance" "example" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = var.instance_name
  }
}


## variables.tf

variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  default     = "ami-0182f373e66f89c85"  # Amazon Linux 2 AMI
}

variable "instance_type" {
  description = "Type of EC2 instance"
  default     = "t2.micro"
}

variable "instance_name" {
  description = "Name tag for the EC2 instance"
  default     = "PatEC2Instance"
}

## outputs.tf

output "instance_id" {
  description = "The ID of the EC2 instance"
  value       = aws_instance.example.id
}

output "public_ip" {
  description = "The public IP of the EC2 instance"
  value       = aws_instance.example.public_ip
}


# deploy-ec2

# main.tf

module "ec2_instance" {
  source         = "../terraform-ec2-module"
  region         = "us-east-1"
  ami_id         = "ami-0182f373e66f89c85"
  instance_type  = "t2.micro"
  instance_name  = "MyDeployedEC2"
}

output "instance_id" {
  value = module.ec2_instance.instance_id
}

output "public_ip" {
  value = module.ec2_instance.public_ip
}


Result: An ec2 instance was deployed. 