Day 12: Zero-Downtime Deployment with Terraform
Name: Udeh Samuel Chibuike
Task Completed: I used Terraform to deploy infrastructure updates with zero downtime using the Implement blue/green deployment
Date and Time: 1/1/2025 10:35pm


provider "aws" {
  region = "us-east-1"
}

# Create Blue Environment
resource "aws_instance" "app_blue" {
  ami           = "ami-01816d07b1128cd2d"  
  instance_type = "t2.micro"
  tags = {
    Name = "app-blue"
  }
}

# Create Green Environment
resource "aws_instance" "app_green" {
  ami           = "ami-0e2c8caa4b6378d8c"   
  instance_type = "t2.micro"
  tags = {
    Name = "app-green"
  }
}

# Create Load Balancer
resource "aws_elb" "app_lb" {
  name               = "app-load-balancer"
  availability_zones = ["us-east-1a", "us-east-1b"]

  listener {
    instance_port     = 80
    instance_protocol = "HTTP"
    lb_port           = 80
    lb_protocol       = "HTTP"
  }

  health_check {
    target              = "HTTP:80/"
    interval            = 30
    timeout             = 5
    healthy_threshold  = 2
    unhealthy_threshold = 2
  }

  instances = [aws_instance.app_blue.id, aws_instance.app_green.id]
}