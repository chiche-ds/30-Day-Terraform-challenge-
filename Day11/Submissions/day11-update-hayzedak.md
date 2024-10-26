# Day 7: Understanding Terraform State

## Participant Details
- **Name:** Akintola AbdulAzeez 
- **Task Completed:** : Use conditionals to deploy resources in a specific environment 
- **Date and Time:** 14-10-2024 04:50 PM

## modules.tf
 ```
resource "aws_instance" "dev_instance" {
  count         = var.environment == "dev" && var.create_ec2_instance ? var.instance_count : 0
  ami           = var.ami_id
  instance_type = var.instance_type
  tags = {
    Name = "dev-instance-${count.index + 1}"
  }
}

resource "aws_instance" "prod_instance" {
  count         = var.environment == "prod" && var.create_ec2_instance ? var.instance_count : 0
  ami           = var.ami_id
  instance_type = var.instance_type
  tags = {
    Name = "prod-instance-${count.index + 1}"
  }
}

variable "instance_type" {}
variable "ami_id" {}
variable "instance_count" {}
variable "create_ec2_instance" {}
variable "environment" {}
```
## main.tf
```
module "ec2_instance" {
  source = "./terraform-modules/ec2-instance"
  instance_count      = var.instance_count
  create_ec2_instance = var.create_ec2_instance
  instance_type       = var.instance_type
  environment         = var.environment
  ami_id              = var.ami_id
}
variable "region" {
  description = "The AWS region to deploy resources in"
  default     = "us-east-1"
}

variable "instance_count" {
  description = "Number of EC2 instances to deploy"
  default     = 1
}

variable "instance_type" {
  description = "The EC2 instance type"
  default     = "t2.micro"
}

variable "create_ec2_instance" {
  description = "Whether to create EC2 instances"
  type        = bool
  default     = true
}

variable "environment" {
  description = "The environment for deployment (dev, staging, production)"
  type        = string
  default     = "dev"
}

variable "ami_id" {
  description = "The AMI ID to use for the EC2 instances"
  type        = string
  default     = "ami-066784287e358dad1"  # Replace with a valid AMI ID
}
```
