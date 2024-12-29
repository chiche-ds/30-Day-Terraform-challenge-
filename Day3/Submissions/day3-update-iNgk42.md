# Day 3: Deploying Basic Infrastructure with Terraform

## Participant Details
- **Name:** NGUEKAM YOSSA Gabin
- **Task Completed:** 
  - **Book:** Chapter 2 of "Terraform: Up & Running" by Yevgeniy (Jim) Brikman 
    - "Deploying a Single Server"
    - "Deploying a Web Server"
  - **Udemy:**
    - "Terraform Plug-in Based Architecture"
    - "Provider Block"
    - "Resource Block"

- **Date and Time:** 23/08/2024 5:00

## Terraform code

```hcl
# Define terraform versions and required providers
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
  region = "eu-west-3"
}

# Fetch ubuntu image from aws
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

# Define security group to allow traffic to our EC2 instance
resource "aws_security_group" "webserver_sg" {
  name        = "webserver_sg"
  description = "Allow traffic from and to the webserver"
}

resource "aws_vpc_security_group_ingress_rule" "allow_traffic_to_webserver" {
  security_group_id = aws_security_group.webserver_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 8000
  ip_protocol       = "tcp"
  to_port           = 8000
}

resource "aws_vpc_security_group_ingress_rule" "allow_ssh" {
  security_group_id = aws_security_group.webserver_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4" {
  security_group_id = aws_security_group.webserver_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv6" {
  security_group_id = aws_security_group.webserver_sg.id
  cidr_ipv6         = "::/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}

# Creates EC2 instance and install nginx
resource "aws_instance" "web" {
  ami             = data.aws_ami.ubuntu.id
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.webserver_sg.name]

  user_data = <<-EOF
    #!/bin/bash

    # Install nginx
    apt-get update && sudo apt-get install -y nginx

    # Customize index.html and listening port
    echo "<h1>Succesfully deployed web server on AWS !</h1>" > /var/www/html/index.html
    sed -i 's/listen 80/listen 8000/' /etc/nginx/sites-enabled/default

    # start nginx
    systemctl restart nginx
  EOF

  user_data_replace_on_change = true

  tags = {
    Name = "web server"
  }
}

# outputs public_ip
output "webserver_public_ip" {
  value = aws_instance.web.public_ip
}
```