# Day 3: Deploying Basic Infrastructure with Terraform

Name: Amudha Balamurugan
Task Completed: Deploying a Single Server" and "Deploying a Web Server"
Date: 8-25-24
Time:08:20 pm






provider "aws" {
  region = "us-east-2"
}

variable "server_port" {
    description = "This port will be used for HTTPS requests"
    type = number
    default = 8080
  
}

output "public_ip" {
  value = aws_instance.example.public_ip
  description = "The public IP address of the web server"
}
resource "aws_instance" "example" {
  ami                    = "ami-0fb653ca2d3203ac1"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.instance.id]

  user_data                   = <<-EOF
                #!/bin/bash
                echo "Hello, World" > index.html
                nohup busybox httpd -f -p ${var.server_port} &
                EOF
  user_data_replace_on_change = true
  tags = {
    Name = "terraform-example"
  }
}

resource "aws_security_group" "instance" {

  name = "terraform-example-instance"

  ingress {
    from_port   = var.server_port
    to_port     = var.server_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
