# Day 5: Scaling Infrastructure

## Name: Njoku Ujunwa Sophia
## Task Completed: Mastering Basic Infrastructure with Terraform
## Date: 8-29-24
## Time: 01:17pm

## Scale your web server cluster using Terraform to handle increased load
```hcl 
provider "aws" {
  region = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance to deploy"
  default     = "t2.micro"
}

variable "ami_id" {
  description = "Amazon Machine Image (AMI) ID"
  default     = "ami-0e86e20dae9224db8"
}

variable "subnet_ids" {
  description = "List of Subnet"
  default     = ["subnet-0b80d1672c1d6452a", "subnet-0846e4641e585a3df"]
}

variable "num_instances" {
  description = "Number of instances in the cluster"
  default     = 2
}

variable "security_group" {
  description = "Security group"
  default     = "sg-0c393266741c7f06a"
}

variable "vpc_id" {
  description = "VPC ID"
  default     = "vpc-03a402beb079dd496"
}

resource "aws_lb" "app_lb" {
  name               = "app-load-balancer"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.security_group]
  subnets            = var.subnet_ids

  enable_deletion_protection = false
  idle_timeout              = 4000
  enable_cross_zone_load_balancing = true

  enable_http2 = true
}

resource "aws_launch_configuration" "app_lc" {
  name          = "app-launch-configuration"
  image_id      = var.ami_id
  instance_type = var.instance_type

  lifecycle {
    create_before_destroy = true
  }

  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y apache2
    systemctl start apache2
    systemctl enable apache2
  EOF
}

resource "aws_autoscaling_group" "app_asg" {
  launch_configuration = aws_launch_configuration.app_lc.id
  min_size             = var.num_instances
  max_size             = var.num_instances
  desired_capacity     = var.num_instances
  vpc_zone_identifier  = var.subnet_ids

  tag {
    key                 = "Name"
    value               = "web-server-instance"
    propagate_at_launch = true
  }

  health_check_type          = "EC2"
  health_check_grace_period  = 300
}

resource "aws_lb_target_group" "app_target_group" {
  name     = "app-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path                = "/"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_target_group.arn
  }
}

resource "aws_autoscaling_policy" "scale_out" {
  name                   = "scale-out"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.app_asg.name
}

resource "aws_autoscaling_policy" "scale_in" {
  name                   = "scale-in"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.app_asg.name
}
