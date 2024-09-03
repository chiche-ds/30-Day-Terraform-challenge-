# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** Njoku Ujunwa Sophia 
- **Task Completed:** Use conditionals to deploy resources only when certain conditions are met
- **Date and Time:** 09/03/2024 01:05 PM

## Using count to Deploy Multiple Instances
### main.tf
```hcl
module "ec2_instance" {
  source          = "./terraform-modules/ec2-instance"
  instance_count  = var.instance_count
  instance_type   = var.instance_type
  region          = var.region
}

variable "region" {
  description = "The AWS region to deploy the instance in"
  default     = "us-east-1"
}

variable "instance_type" {
  description = "The EC2 instance type"
  default     = "t2.micro"
}

variable "instance_count" {
  description = "Number of EC2 instances to deploy"
  default     = 2
}
```
### modules.tf
```hcl
variable "instance_count" {
  description = "Number of EC2 instances to deploy"
  type        = number
  default     = 1
}

variable "region" {}
variable "instance_type" {}

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
  count         = var.instance_count
  ami           = data.aws_ami.latest.id
  instance_type = var.instance_type
  tags = {
    Name = "web-server-${count.index + 1}"
  }
}
```


## Using for_each to Iterate Over Maps or Lists


## Implementing Conditional Logic

