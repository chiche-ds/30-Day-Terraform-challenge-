Name: Sunil Kumar
Task Completed: Read chapter 2 from the book and deployed a web server using Terraform in the AWS cloud.

Date:26/08/2024
Time: 5PM
Terraform code:

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "ap-south-1"
}
#variable declaration
variable "server_port" {
description = "The port the server will use for HTTP requests"
type = number
default = 8080
}
#to display the public IP of the web server
output "public_ip" {
value = aws_instance.my_webserver.public_ip
description = "The public IP address of the web server"
}

resource "aws_instance" "my_webserver" {
  ami                         = "ami-0522ab6e1ddcc7055"
  vpc_security_group_ids      = [aws_security_group.sg1.id]
  instance_type               = "t2.micro"
  
  user_data                   = <<-EOF
#!/bin/bash
echo "Hello, World, I am learning IaC" > index.html
nohup busybox httpd -f -p ${var.server_port} &
EOF
  user_data_replace_on_change = true


  tags = {
    Name = "WebServerInstance"
  }
}
resource "aws_security_group" "sg1" {
  name = "terraform-my_server-instance"
  ingress {
    from_port   = var.server_port
    to_port     = var.server_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

![image](https://github.com/user-attachments/assets/320c3edc-f387-4efe-ab52-c3ab704ff308)
