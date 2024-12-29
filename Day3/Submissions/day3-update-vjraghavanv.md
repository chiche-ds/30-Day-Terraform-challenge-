# Day 3: Deploying Basic Infrastructure with Terraform

## Participant Details

- **Name:** Vijayaraghavan Vashudevan
- **Task Completed:** Learnt - Understanding of Provider block, Resource block, and hands-on of Deployment of web-server using Terraform.
- **Date and Time:** 21-08-2024 at 07:27 am IST

### main.tf
```bash
# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Security Group
resource "aws_security_group" "web-server" {
  vpc_id      =  aws_vpc.vpc.id
  name        = "web-server"
  description = "Allow incoming HTTP Connections"
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Creation of EC2 Instance
resource "aws_instance" "web-server" {
  ami             = "ami-02e136e904f3da870"
  instance_type   = "t2.micro"
  key_name        = "terraform-challenge"
  security_groups = ["${aws_security_group.web-server.name}"]
  user_data       = <<-EOF
#!/bin/bash 
sudo su
yum update -y
yum install httpd -y
systemctl start httpd
systemctl enable httpd
echo "<html><h1> Welcome to #30DaysTerraformChallenge. Happy Learning... </h1></html>" >> /var/www/html/index.html       
EOF 
  tags = {
    Name = "web_instance"
  }
}
```
### terraform.tf
```bash
terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.1.0"
    }
  }
}
```
### output.tf
```bash
output "web_instance_ip" {
  value = aws_instance.web-server.public_ip
}
```
### Architecture/Flow Diagram of Web-App Server using Terraform

![Architecture/Flow Diagram of Web-App Server using Terraform](arch_diagram_vjraghavanv.gif)
