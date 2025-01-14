# Day 5: Scaling Infrastructure

**Name**: Jully Achenchi
**Task Completed**: Mastering Basic Infrastructure with Terraform
**Date**: 11/12/2024

## Scale your web server cluster using Terraform to handle increased the load

### main.tf
```hcl 
provider "aws" {
  region = var.region
}

resource "aws_launch_template" "clustered_web" {
  name          = "ClusteredWebServer"
  image_id      = var.ami_id
  instance_type = var.instance_type

  user_data = base64encode(<<-EOF
              #!/bin/bash
              apt update
              apt install -y nginx
              systemctl start nginx
              systemctl enable nginx
              echo "Hello from $(hostname)" > /var/www/html/index.html
              EOF
  )

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.web.id]
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "ClusteredWebServer"
    }
  }
}

resource "aws_autoscaling_group" "clustered_web_group" {
  name                = "ClusteredWebServerASG"
  vpc_zone_identifier = var.subnet_ids
  target_group_arns   = [aws_lb_target_group.web.arn]

  launch_template {
    id      = aws_launch_template.clustered_web.id
    version = "$Latest"
  }

  min_size         = var.cluster_min_size
  max_size         = var.cluster_max_size
  desired_capacity = var.cluster_desired_capacity

  health_check_type         = "ELB"
  health_check_grace_period = 300

  tag {
    key                 = "Name"
    value               = "ClusteredWebServer"
    propagate_at_launch = true
  }
}

resource "aws_lb" "web" {
  name               = "clustered-web-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.subnet_ids
}

resource "aws_lb_listener" "web" {
  load_balancer_arn = aws_lb.web.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}

resource "aws_lb_target_group" "web" {
  name     = "clustered-web-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path                = "/"
    healthy_threshold   = 2
    unhealthy_threshold = 10
  }
}

resource "aws_security_group" "web" {
  name        = "allow_web_traffic"
  description = "Allow inbound web traffic"
  vpc_id      = var.vpc_id

  ingress {
    description     = "HTTP from ALB"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "alb" {
  name        = "allow_alb_traffic"
  description = "Allow inbound ALB traffic"
  vpc_id      = var.vpc_id

  ingress {
    description = "HTTP from anywhere"
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

```



### variables.tf

```hcl

variable "region" {
  description = "The AWS region to deploy the resources."
  default     = "us-east-1"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instances."
  type        = string
  default     = "ami-0866a3c8686eaeeba"
}

variable "instance_type" {
  description = "The instance type for the EC2 instances."
  default     = "t2.micro"
}

variable "cluster_min_size" {
  description = "Minimum size of the auto-scaling group."
  type        = number
  default     = 2
}

variable "cluster_max_size" {
  description = "Maximum size of the auto-scaling group."
  type        = number
  default     = 5
}

variable "cluster_desired_capacity" {
  description = "Desired capacity of the auto-scaling group."
  type        = number
  default     = 3
}

variable "subnet_ids" {
  description = "List of subnet IDs for the auto-scaling group."
  type        = list(string)
  default     = ["subnet-028e72cd50eafc8ca", "subnet-06e9ada92d8ef92e8"]
}

variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
  default = "vpc-076480c307135d35d"
}

```


