# Day 8: Reusing Infrastructure with Modules

## Participant Details
- **Name:** Akintola AbdulAzeez 
- **Task Completed:** Terraform module for EC2 instance
- **Date and Time:** 13/10/2024 06:25 AM

## main.tf
```
provider "aws" {
  region = var.region
}

resource "aws_instance" "this" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = var.security_group_ids

  tags = {
    Name = var.instance_name
  }
}
```

## variables.tf

````
variable "ami_id" {
  description = "The ID of the AMI to use for the EC2 instance."
  type        = string
}

variable "instance_type" {
  description = "The instance type to use for the EC2 instance."
  type        = string
  default     = "t2.micro"
}

variable "instance_name" {
  description = "The name to assign to the EC2 instance."
  type        = string
}

variable "region" {
  description = "The AWS region to deploy resources."
  type        = string
  default     = "us-east-1"
}

variable "subnet_id" {
  description = "The ID of the subnet in which to launch the instance."
  type        = string
}

variable "security_group_ids" {
  description = "The security group IDs to associate with the instance."
  type        = list(string)
}
```

## outputs.tf

```
output "instance_id" {
  description = "The ID of the EC2 instance."
  value       = aws_instance.this.id
}

output "public_ip" {
  description = "The public IP of the EC2 instance."
  value       = aws_instance.this.public_ip
}
```

The main.tf file that calls the module

```
provider "aws" {
  region = "us-east-1"
}


module "ec2_instance" {
  source             = "./terraform-aws-ec2"
  ami_id             = "ami-06b21ccaeff8cd686"
  instance_type      = "t2.micro"
  instance_name      = "MyEC2Instance"
  subnet_id          = "subnet-08a604e869c0ccd2b"
  security_group_ids = ["sg-0040022bca3d48b8d"]
}

output "instance_id" {
  value = module.ec2_instance.instance_id
}

output "public_ip" {
  value = module.ec2_instance.public_ip
}
```