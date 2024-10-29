# Day 16:  Building Production-Grade Infrastructure
## Participant Details

- **Name:** Maryjane Enechukwu 
- **Task Completed:**"modules 

- **Date and Time:** 23/10/2024 

# main.tf in modules/ec2_instance
```
hcl

variable "instance_type" {
  description = "The type of instance to use"
  type        = string
  default     = "t2.micro"
}

variable "ami" {
  description = "AMI ID for the instance"
  type        = string
}

resource "aws_instance" "instance" {
  ami           = var.ami
  instance_type = var.instance_type

  tags = {
    Name = "Instance-${var.instance_type}"
  }
}
```

# variables.tf

```
hcl

variable "instance_type" {
  description = "The type of instance to use"
  type        = string
}

variable "ami" {
  description = "The AMI ID to use for the instance"
  type        = string
}
```

# modules.tf 
```
hcl
module "ec2_instance" {
  source        = "../modules/ec2_instance"
  instance_type = "t3.micro"
  ami           = "ami-12345678"
}
```

# provider.tf
```
hcl

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.0.0"
}
```

# a github workflow
```
hcl

name: Terraform CI

on:
  push:
    branches:
      - main

jobs:
  terraform:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v1

      - name: Terraform Init
        run: terraform init

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        run: terraform plan

      - name: Terraform Apply (Auto Approve)
        run: terraform apply -auto-approve
```

https://github.com/Lumen-jane/Terraform-AWS-EC2-Module.git