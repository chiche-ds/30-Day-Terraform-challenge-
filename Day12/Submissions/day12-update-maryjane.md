# Day 12: Zero-Downtime Deployment with Terraform


## Participant Details

- **Name:** Maryjane Enechukwu
- **Task Completed:** Deploying a web application with canary releases, ensuring that infrastructure updates cause no service interruptions.
- **Date and Time:** 22/10/2024 06:30 PM 

main.tf
```hcl
variable "region" {
  description = "The AWS region to deploy resources in"
  default     = "us-east-1"
}

variable "instance_type" {
  description = "The EC2 instance type"
  default     = "t2.micro"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance"
  default     = "ami-066784287e358dad1"
}

variable "security_groups" {
  description = "Security group IDs for the EC2 instances"
  type        = list(string)
  default     = ["sg-0c393266741c7f06a"]
}

variable "vpc_id" {
  description = "The VPC ID"
  default     = "vpc-03a402beb079dd496"
}

variable "subnets" {
  description = "The Subnet IDs for the load balancer"
  type        = list(string)
  default     = ["subnet-0846e4641e585a3df", "subnet-0b80d1672c1d6452a"]
}

variable "canary_percent" {
  description = "Percentage of traffic to route to the canary release"
  type        = number
  default     = 10
}

resource "aws_instance" "old_version" {
  ami               = var.ami_id
  instance_type     = var.instance_type
  count             = 1
  vpc_security_group_ids = var.security_groups  # Correct parameter

  tags = {
    Name = "old-instance"
  }
}

resource "aws_instance" "canary_version" {
  ami               = var.ami_id
  instance_type     = var.instance_type
  count             = 1
  vpc_security_group_ids = var.security_groups  # Correct parameter

  tags = {
    Name = "canary-instance"
  }
}


# Create a load balancer
resource "aws_lb" "canary_lb" {
  name               = "canary-load-balancer"
  internal           = false
  load_balancer_type = "application"
  security_groups    = var.security_groups
  subnets            = var.subnets
}

# Target group for the old version
resource "aws_lb_target_group" "old_version_tg" {
  name     = "old-version-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
}

# Target group for the canary version
resource "aws_lb_target_group" "canary_version_tg" {
  name     = "canary-version-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.canary_lb.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.old_version_tg.arn
  }
}

resource "aws_lb_listener_rule" "canary_traffic" {
  listener_arn = aws_lb_listener.http.arn
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.canary_version_tg.arn
  }
  condition {
    path_pattern {
      values = ["*"]
    }
  }
}
```
