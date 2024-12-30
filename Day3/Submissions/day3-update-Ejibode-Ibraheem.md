# Day 3: Deploying Basic Web Server Infrastructure with terraform 
## Participant details 
* Name: Ejibode Ibraheem
* Task: Basic web server
* Date: 12/4/2024



provider "aws" {
  region = "eu-north-1"
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
  ami           = "ami-0e86e20dae9224db8"
  instance_type = "t2.micro"

  security_groups = [aws_security_group.web_sg.name]

  # User data script for Ubuntu to install Nginx
  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install apache2 -y
              sudo systemctl start apache2
              sudo systemctl enable apache2
              echo "<h1> Hi, and welcome to my day 3 terraform challenge </h1>" | sudo tee /var/www/html/index.html
              EOF

  tags = {
    Name = "Terraform Web Server "
  }
}