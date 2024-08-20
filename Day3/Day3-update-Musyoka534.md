# Day 3: Deploying Basic Infrastructure with Terraform

## Participant Details
- **Name:** Musyoka Kilonzo
- **Task Completed:** Read chapter 2 of the book provided and focused on "Deploying a Single Server" and "Deploying a Web Server.",Provisioned AWS EC2 server and setup a basic web server using Terraform.
- **Date and Time:** 20/08/2024 16:00 PM


# Terraform Code Update

## Overview

This document provides details on the Terraform configuration used to deploy an EC2 instance with a basic web server setup on AWS. The configuration includes provisioning an EC2 instance and setting up a security group to allow HTTP and SSH access.

## Changes Made

### Resources

1. **AWS EC2 Instance**
   - **Description**: Creates an EC2 instance running an Nginx web server.
   - **AMI**: `ami-04a81a99f5ec58529` (Specify the AMI ID for the instance)
   - **Instance Type**: `t2.micro`
   - **Key Name**: `musyoka`
   - **Availability Zone**: `us-east-1a`
   - **Security Group**: Attached to `aws_security_group.web-server-sg`
   - **User Data**: Script to install and start Nginx.

2. **AWS Security Group**
   - **Description**: Defines security rules to allow HTTP and SSH traffic.
   - **Inbound Rules**:
     - Port 22 (SSH) from `0.0.0.0/0`
     - Port 80 (HTTP) from `0.0.0.0/0`
   - **Outbound Rules**: Allow all outbound traffic.

## Code

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Create an EC2 instance
resource "aws_instance" "web-server" {
  ami               = "ami-04a81a99f5ec58529"
  instance_type     = "t2.micro"
  key_name          = "musyoka"
  availability_zone = "us-east-1a"
  vpc_security_group_ids = [aws_security_group.web-server-sg.id]

  user_data                   = <<-EOF
    #!/bin/bash
    sudo apt-get update
    sudo apt-get install -y nginx
    sudo systemctl start nginx
    sudo systemctl enable nginx
  EOF
  user_data_replace_on_change = true
  
  tags = {
    Name = "web-server"
  }
}

# Security group to allow HTTP and SSH protocols
resource "aws_security_group" "web-server-sg" {
  name = "web-server-sg"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
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
