# Day 4: Mastering Basic Infrastructure with Terraform

## Name: Maryjane Enechukwu
## Task Completed: Mastering Basic Infrastructure with Terraform
## Date: 9-10-24
## Time: 5:00pm

## Deploy a configurable and clustered web server using Terraform.
# main.tf 

provider "aws" {
  region = var.region
}

resource "aws_instance" "configurable_web" {
  ami           = var.ami_id
  instance_type = var.instance_type

  security_groups = [aws_security_group.web_sg.name]

  tags = {
    Name = "ConfigurableWebServer"
  }

  user_data = <<-EOF
              #!/bin/bash
              apt update
              apt install -y nginx
              systemctl start nginx
              systemctl enable nginx
              EOF
}

# Security Group

resource "aws_security_group" "web_sg" {

  name        = "web_sg"
  description = "Allow HTTP and SSH"


  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow HTTP from anywhere
  }

}

# variables.tf 
variable "region" {
  description = "The AWS region to deploy the resources."
  default     = "us-east-1"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance."
  default     = "ami-0866a3c8686eaeeba"  
}

variable "instance_type" {
  description = "The instance type for the EC2 instance."
  default     = "t2.micro"
}

# output.tf

output "configurable_web_server_public_ip" {
  description = "Public IP of the configurable web server."
  value       = aws_instance.configurable_web.public_ip
}