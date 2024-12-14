### Name: God'sfavour Braimah
### Task: Day 8: Reusing Infrastructure with Modules
### Date: 12/11/24
### Time: 10:15pm
 ### Activity

### Created a Module:

Module Name: VPC and EC2 Module

Built a basic Terraform module for creating a VPC and an EC2 instance.

Deployed Infrastructure Using the Module:

Used the newly created module to deploy:

A VPC with a subnet.

An EC2 instance within the VPC.

### Highlights:

Implemented reusable modules.

Mapped variables using terraform.tfvars for better flexibility.

Verified infrastructure deployment on AWS.
### Modules
```
provider "aws" {
  region = "us-east-1"
}

module "main" {
  source            = "./modules/vpc"
  cidr_block        = var.vpc_cidr_block
  vpc_name          = var.vpc_name
  subnet_cidr       = var.subnet_cidr
  availability_zone = var.availability_zone
  subnet_name       = var.subnet_name
}

module "web" {
  source        = "./modules/ec2"
  ami           = var.ami
  key_name      = var.key_name
  instance_type = var.instance_type
  subnet_id     = module.vpc.subnet_id
 instance_name = var.instance_name
}
```

### The Variales 
```
 variable "vpc_cidr_block" {}
variable "vpc_name" {}
variable "subnet_cidr" {}
variable "availability_zone" {}
variable "subnet_name" {}
variable "ami" {}
variable "key_name" {}
variable "instance_type" {}
variable "instance_name" {}
```