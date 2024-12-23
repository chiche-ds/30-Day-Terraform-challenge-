# Day 14: Building Production-Grade Infrastructure

## Participant Details

- **Name:** Ejibode Ibraheem A
- **Task Completed:** Building Production-Grade Infrastructure
- **Date and Time:** 23/12/2024 6:11 PM


## main.tf
```
provider "aws" {
  region = "us-east-1"
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = var.vpc-name
  cidr = var.cidr

  azs             = var.azs
  private_subnets = var.private
  public_subnets  = var.public

  tags = {
    Terraform   = var.tag
    Environment = var.env
  }
}

module "ec2_instance" {
  source = "terraform-aws-modules/ec2-instance/aws"

  name = var.name

  instance_type          = var.instance_type
  vpc_security_group_ids = [var.sg]
  subnet_id              = var.subnet_id
  ami                    = var.ami
  tags = {
    Terraform   = var.tag
    Environment = var.env
  }
}
```

## variables.tf
```
variable "cidr" {
  type    = string
  default = ""
}
variable "vpc-name" {
  type    = string
  default = ""
}

variable "azs" {
  type    = list(string)
  default = [""]
}

variable "private" {
  type    = list(string)
  default = [""]
}

variable "public" {
  type    = list(string)
  default = [""]
}

variable "env" {
  type    = string
  default = ""
}

variable "tag" {
  type    = bool
  default = ""
}
variable "subnet_id" {
  type    = string
  default = ""
}

variable "instance_type" {
  type    = string
  default = ""
}

variable "sg" {
  type    = string
  default = ""
}

variable "name" {
  type    = string
  default = ""
}

variable "ami" {
  type    = string
  default = ""
}

```

## terraform.tfvars
```
azs           = ["us-east-1a", "us-east-1b", "us-east-1c"]
private       = ["10.0.6.0/24", "10.0.7.0/24", "10.0.8.0/24"]
public        = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
env           = "dev"
cidr          = "10.0.0.0/16"
subnet_id     = "subnet-059d650d330b4584a"
ami           = "ami-0e86e20dae9224db8"
instance_type = "t2.micro"
sg            = "sg-0d4c0510df5f61e80"
vpc-name      = "test-stage"
tag           = true
```

## workflow
```
name: terraform config

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  terraform-test:
    name: terraform 
    runs-on: ubuntu-latest
    steps:
    - name: checking repo
      uses: actions/checkout@v2

    - name: setting up terraform 
      uses: hashicorp/setup-terraform@v3
      with:
        terraform_version: "1.1.7"

    - name: AWs setup
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1

    - name: Terraform init 
      run: terraform init

    - name: Terraform plan
      run: terraform plan
```
