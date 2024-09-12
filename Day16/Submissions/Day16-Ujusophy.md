# Day 16: Building Production-Grade Infrastructure
## Participant Details

- **Name:** Njoku Ujunwa Sophia 
- **Task Completed:** Refactored the code to be used in a production-grade standards.
- **Date and Time:** 12/09/2024 01:02 PM


## terraform/modules/provider/main.tf
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
output "instance_id" {output "instance_id" {
  description = "The ID of the EC2 instance"
  value       = aws_instance.this.id
}
```

## terraform/main.tf
```hcl
module "provider" {module "provider" {
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
variable "region" {variable "region" {
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


A simple GitHub Actions CI pipeline could look like this:

## .github/workflows/terraform.yml
```yaml
name: 'Terraform CI'name: 'Terraform CI'

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  terraform:
    name: 'Terraform Plan'
    runs-on: ubuntu-latest

    steps:
      - name: 'Checkout Code'
        uses: actions/checkout@v3

      - name: 'Setup Terraform'
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.0

      - name: 'Terraform Init'
        run: terraform init

      - name: 'Terraform Format Check'
        run: terraform fmt -check

      - name: 'Terraform Validate'
        run: terraform validate

      - name: 'Terraform Plan'
        run: terraform plan
```
