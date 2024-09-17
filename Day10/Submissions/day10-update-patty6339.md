# Day 9: Terraform Loops and Conditionals

## Participant Details

- **Name:** Patrick Odhiambo
- **Task Completed:** Terraform Loops and Conditionals
- **Date and Time:** 16/9/24 at 8:30 pm

## Terraform Code 

### Updated main.tf (with loop and conditionals)

provider "aws" {
  region = var.region
}

resource "aws_instance" "example" {
  count = var.create_instance ? 1 : 0  # Conditional resource creation

  ami           = var.ami_id
  instance_type = var.instance_type

  tags = { for k, v in var.instance_tags : k => v }  # Loop to set tags

  lifecycle {
    prevent_destroy = var.prevent_destroy  # Conditional lifecycle policy
  }
}


### Updated variables.tf (supporting dynamic tags and conditionals)

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

variable "instance_tags" {
  description = "A map of tags to apply to the instance"
  type        = map(string)
  default     = {
    Name = "PatEC2Instance"
    Env  = "dev"
  }
}

variable "create_instance" {
  description = "Flag to create an EC2 instance"
  type        = bool
  default     = true
}

variable "prevent_destroy" {
  description = "Flag to prevent destroying the instance"
  type        = bool
  default     = false
}

### Updated outputs.tf

output "instance_id" {
  description = "The ID of the EC2 instance"
  value       = aws_instance.example[0].id
  condition   = length(aws_instance.example) > 0  # Ensure instance exists
}

output "public_ip" {
  description = "The public IP of the EC2 instance"
  value       = aws_instance.example[0].public_ip
  condition   = length(aws_instance.example) > 0  # Ensure instance exists
}

### Updated deploy-ec2/main.tf (calling the module)

module "ec2_instance" {
  source  = "../terraform-ec2-module"
  version = "1.0.0"

  region          = "us-east-1"
  ami_id          = "ami-0182f373e66f89c85"
  instance_type   = "t2.micro"
  instance_name   = "MyDeployedEC2"
  create_instance = true
  prevent_destroy = false
  instance_tags   = {
    Name = "MyDeployedEC2"
    Env  = "prod"
  }
}

output "instance_id" {
  value = module.ec2_instance.instance_id
}

output "public_ip" {
  value = module.ec2_instance.public_ip
}


