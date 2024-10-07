# Day 3: Deploy Basic Infrastructure - Terraform

## Participant Details
- **Name:** Ajibola Mubarak
- **Task Completed:** Watched videos 11, 12, 13  
  Read Chapter 2

- **Date:** 07-10-2024

## main.tf

```hcl
provider "aws" {
  region = "us-east-1"
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

  ingress {
    protocol  = -1
    self      = true
    from_port = 0
    to_port   = 0
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web-server" {
  ami           = "ami-04a81a99f5ec58529"
  instance_type = "t2.micro"

  security_groups = [aws_security_group.web_sg.name]

  # User data script for Ubuntu to install Nginx
  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install nginx -y
              sudo systemctl start nginx
              sudo systemctl enable nginx
              echo "<h1>Hello, Mubarak welcome to Terraform</h1>" | sudo tee /var/www/html/index.html
              EOF

  tags = {
    Name = "Terraform Web Server"
  }
}
