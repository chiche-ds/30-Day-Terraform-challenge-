# Day 4: Mastering Basic Infrastructure with Terraform

## Name: Njoku Ujunwa Sophia
## Task Completed: Mastering Basic Infrastructure with Terraform
## Date: 8-29-24
## Time: 01:17pm

Today I tried using the input variabeles to deploy the web server
```
provider "aws" {
    region = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance to deploy"
  type     = string
}

variable "ami_id" {
  description = "Amazon Machine Image (AMI) ID"
  type   = string  
}

variable "subnet_id" {
  description = "Subnet"
  type     = string  
}

variable "security_group" {
  description = "Security group"
  type     = string  
}

resource "aws_instance" "web_server" {
    ami = var.ami_id
    subnet_id = var.subnet_id
    instance_type = var.instance_type
    security_groups = [var.security_group]
    tags = {
        first = "web_server"
    }
  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y apache2
    systemctl start apache2
    systemctl enable apache2
  EOF
}
```
