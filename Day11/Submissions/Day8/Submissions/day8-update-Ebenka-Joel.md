# Day 8: Reusing Infrastructure with Modules
## Participant Details

- **Name:** Ebenka christian 
- **Date and Time:** 09-09-2024 at 02:42 am
- **Task Completed:** 

1. **Reading**:  Chapter 4 (Pages 115-139) Focus on these sections ( How to Create Reusable Infrastructure with Terraform Modules)
   - Sections: "Module Basics", "Inputs", and "Outputs".


3. **Activity**: 
   - Create a basic Terraform module for a common infrastructure component (e.g., an EC2 instance, VPC, load balancer).
   - Deploy infrastructure using the module.



Create a basic Terraform module for a common infrastructure component: let use a simple code to launch an ec2 server on aws
here is a suggested structure of our module

https://registry.terraform.io/modules/terraform-aws-modules/ec2-instance/aws/latest

terraform-ec2-instance/
├── main.tf
├── variables.tf
├── outputs.tf
└── README.md


main.tf

```hcl

## Author Joel Ebenka 
provider "aws" {
  region = var.region
}

resource "aws_instance" "ec2_instance" {
  ami           = var.ami
  instance_type = var.instance_type

  tags = {
    Name = var.instance_name
  }
}
```

variable.tf

```hcl

## Author Joel Ebenka 

variable "region" {
  description = "The AWS region to deploy the EC2 instance."
  type        = string
  default     = "us-east-1"
}

variable "ami" {
  description = "The AMI to use for the EC2 instance."
  type        = string
}

variable "instance_type" {
  description = "The type of instance to start."
  type        = string
  default     = "t2.micro"
}

variable "instance_name" {
  description = "The name of the EC2 instance."
  type        = string
}
```

output.tf

```hcl

## Author Joel Ebenka 
output "instance_id" {
  description = "The ID of the EC2 instance."
  value       = aws_instance.ec2_instance.id
}

output "public_ip" {
  description = "The public IP address of the EC2 instance."
  value       = aws_instance.ec2_instance.public_ip
}
```

module.tf

```hcl

# Terraform EC2 Instance Module

#This module deploys an EC2 instance on AWS.
##https://registry.terraform.io/modules/terraform-aws-modules/ec2-instance/aws/latest
module "ec2_instance" {
  source        = "terraform-aws-modules/ec2-instance/aws"
  ami           = "ami-0182f373e66f89c85"
  instance_type = "t2.micro"
  name = "30daysterraform"
}
```
