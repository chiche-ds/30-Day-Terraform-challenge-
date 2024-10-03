# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** Salako Lateef
- **Task Completed:** Conditional Deployments
- **Date and Time:** 2024-10-03 08:54 AM GMT

## Count main.tf
```
provider "aws" {
  region = var.region
}

resource "aws_instance" "web" {
  count = var.env == "dev" ? 1 : 4

  ami = var.ami
  instance_type = var.instance_type
  subnet_id = var.subnet
  vpc_security_group_ids = [var.sg]

  tags = {
    Name = "web-${count.index + 1}"
  }
}
variable "region" {
  type = string
  default = "us-east-1"
}

variable "ami" {
  type = string
  default = "ami-0e86e20dae9224db8"
}

variable "env" {
  type = string
  default = "prod"

  validation {
    condition = contains(["dev", "prod"], var.env)
    error_message = "input only dev or prod"
  }
}

variable "instance_type" {
  type = string 
  default = "t2.micro"
}

variable "sg" {
  type = string
  default = "sg-0ed7b0e6d5df0a363"
}

variable "subnet" {
  type = string 
  default = "subnet-03cb68d25e5198c95"
}
```

## for_each main.tf
```
variable "ami" {
  type = string
  default = "ami-0e86e20dae9224db8"
}

variable "instance_type" {
  type = string 
  default = "t2.micro"
}

variable "sg" {
  type = string
  default = "sg-0ed7b0e6d5df0a363"
}

variable "subnet" {
  type = map(any)
  default = {
    dev = "subnet-03cb68d25e5198c95"
    prod = "subnet-03cb68d65e51e8c62"
  }
}

resource "aws_instance" "key" {
  for_each =  var.subnet
  ami = var.ami
  security_groups = [var.sg]
  subnet_id = each.value
}
```
