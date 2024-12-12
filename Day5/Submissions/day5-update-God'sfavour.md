## Participant Details
- **Name:** God'sfavour Braimah
# Day 5: Scaling Infrastructure with Terraform  
### Terraform 30-Day Challenge
## Date: 12-7-2024
## Time: 07:20AM

## Overview  
Welcome to Day 5 of the Terraform 30-Day Challenge! Today’s focus was on scaling infrastructure to handle increased load and understanding the importance of Terraform’s state. This project demonstrates how to use Terraform to deploy and scale a highly available infrastructure with an AWS Application Load Balancer (ALB) and an Auto Scaling Group (ASG).  

---

## Features  
- **Application Load Balancer (ALB)**: Distributes traffic across multiple instances to handle increased load.  
- **Auto Scaling Group (ASG)**: Dynamically scales the web server cluster to maintain performance.  
- **Security Groups**: Ensures secure communication by managing ingress and egress traffic.  
- **Terraform State Management**: Focuses on the importance of Terraform’s state file for infrastructure tracking.  

---

## Prerequisites  
1. Terraform installed on your local machine.  
2. AWS CLI configured with proper credentials.  
3. An AWS Key Pair for SSH access to the EC2 instances.  

---

## Terraform Code Structure  
- **Provider Block**: Specifies AWS as the provider and the deployment region.  
- **Data Blocks**: Fetches the default VPC and its associated subnets.  
- **Resources**:  
  - `aws_lb`: Creates an ALB to distribute traffic.  
  - `aws_security_group`: Configures secure access to the ALB.  
  - `aws_launch_configuration`: Defines the configuration for EC2 instances.  
  - `aws_autoscaling_group`: Dynamically scales instances based on load.  
  - `aws_lb_target_group`: Associates the ASG with the ALB.  
  - `aws_lb_listener`: Configures the ALB listener for routing traffic.  
- **Output Block**: Outputs the DNS name of the ALB.  

---

```
   provider "aws" {
  region = var.region # Use a variable to specify the region
}

# Fetch the default VPC
data "aws_vpc" "default" {
  default = true
}

# Fetch subnets associated with the default VPC
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Application Load Balancer
resource "aws_lb" "example" {
  name               = "terraform-asg-example"
  load_balancer_type = "application"
  subnets            = data.aws_subnets.default.ids
  security_groups    = [aws_security_group.alb.id]
}

# Security Group for ALB
resource "aws_security_group" "alb" {
  name = "terraform-example-alb"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.cidr_blocks]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.cidr_blocks]
  }
}

# Target Group for ASG
resource "aws_lb_target_group" "asg" {
  name     = "terraform-asg-example"
  port     = var.server_port
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.default.id

  health_check {
    path                = "/"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 15
    timeout             = 3
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

# Listener for ALB
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.example.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "404: page not found"
      status_code  = "404"
    }
  }
}

# Listener Rule for Target Group
resource "aws_lb_listener_rule" "asg" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 100

  condition {
    path_pattern {
      values = ["*"]
    }
  }

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.asg.arn
  }
}

# Launch Configuration for Auto Scaling Group

resource "aws_launch_template" "example" {
  name          = "example-launch-template"
  image_id      = var.ami_id # Specify the AMI ID as a variable
  instance_type = "t2.micro"

  # User Data to set up the instance
  user_data = <<-EOF
              #!/bin/bash
               sudo yum update -y
               sudo yum install -y httpd
               sudo systemctl start httpd
               sudo systemctl enable httpd
               echo "Hello, World" > /var/www/html/index.html
  EOF



  # Optional key pair for SSH access
  key_name = var.key_name # Optional variable for the EC2 key pair
}

# Autoscaling Group
resource "aws_autoscaling_group" "example" {
  launch_template {
    id      = aws_launch_template.example.id
    version = "$Latest"
  }

  vpc_zone_identifier  = data.aws_subnets.default.ids
  target_group_arns    = [aws_lb_target_group.asg.arn]
  health_check_type    = "ELB"
  min_size             = 2
  max_size             = 10

  tag {
    key                 = "Name"
    value               = "terraform-asg-example"
    propagate_at_launch = true
  }
}

# Output DNS Name of ALB
output "alb_dns_name" {
  value       = aws_lb.example.dns_name
  description = "The domain name of the load balancer"
}

variable "region" {
  default = "us-east-1"
}

variable "cidr_blocks" {
  default = "0.0.0.0/0"
}

variable "ami_id" {
  description = "The AMI ID to use for the launch configuration."
  default = "ami-0453ec754f44f9a4a"
}

variable "server_port" {
  description = "The port for the web server."
  default     = 80
}

variable "key_name" {
  description = "The name of the EC2 key pair to use for SSH access."
  default     = null
}

```
