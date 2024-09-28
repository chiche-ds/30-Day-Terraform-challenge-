# Day 8: Reusing Infrastructure with Modules

## Participant Details

- **Name:** Duncan Gaturu
- **Task Completed:**  i managed to cover the topic : Understand how to create reusable modules in Terraform, define input variables, and output values from modules and terraform module sources.
- **Date and Time:** 17-09-2024 at 22:19 pm 

### main.tf
```
# main.tf
provider "aws" {
  region = var.region
}

resource "aws_instance" "ec2_instance" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = var.instance_name
  }
}

```
### variables.tf
```
# variables.tf

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "instance_name" {
  description = "Name tag for the instance"
  type        = string
}

```
### main.tf
```
module "my_ec2_instance" {
  source        = "./terraform-ec2-module"
  ami_id        = "ami-0e86e20dae9224db8" 
  instance_name = "MyInstance"
}


```
### output.tf
```
# outputs.tf

output "instance_id" {
  description = "The ID of the EC2 instance"
  value       = aws_instance.ec2_instance.id
}

output "public_ip" {
  description = "The public IP of the EC2 instance"
  value       = aws_instance.ec2_instance.public_ip
}

```
