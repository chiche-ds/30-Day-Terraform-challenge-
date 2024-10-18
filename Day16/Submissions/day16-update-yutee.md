# Day 16: Building Production-Grade Infrastructure

## Participant Details

- **Name:** Utibe Okon (yutee)
- **Task Completed:** Edited code to be production-grade ready
- **Date and Time:** Mon 15th October, 2024 | 1:04 PM GMT+1

### Overview
Production level infra is scary. If I just joined a company I would not like if my code is used in production. I would not want to be the source of my company's download. But after this task, I felt a bit more confident about building things that can actually be used in production. best practices, security and proper documentation.

I got to understand that production grade code goes beyond just writing code that works. It encompasses a lot of different moving parts and involves a lot including versioning and testing.

## Terraform Code 
```hcl
provider "aws" {
  region = var.region
}
```

## terraform/modules/provider/variables.tf
```hcl
variable "region" {
  description = "The AWS region to deploy resources"
}
```

## terraform/modules/ec2-instance/main.tf
```hcl
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

resource "aws_instance" "this" {
  ami           = data.aws_ami.latest.id
  instance_type = var.instance_type
  tags = {
    Name = "production-instance"
  }
}
```

## terraform/modules/ec2-instance/variables.tf
```hcl
variable "instance_type" {
  description = "The EC2 instance type"
}
```

## terraform/modules/ec2-instance/outputs.tf
```hcl
output "instance_id" {
  description = "The ID of the EC2 instance"
  value       = aws_instance.this.id
}
```

## terraform/main.tf
```hcl
module "provider" {
  source  = "./modules/provider"
  region  = var.region
}

module "ec2_instance" {
  source          = "./modules/ec2-instance"
  instance_type   = var.instance_type
  region          = var.region
}

output "ec2_instance_id" {
  description = "The ID of the EC2 instance"
  value       = module.ec2_instance.instance_id
}
```

## terraform/variables.tf
```hcl
variable "region" {
  description = "The AWS region to deploy the instance in"
  default     = "us-east-1"
}

variable "instance_type" {
  description = "The EC2 instance type"
  default     = "t2.micro"
}
```

## terraform/versions.tf
```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```