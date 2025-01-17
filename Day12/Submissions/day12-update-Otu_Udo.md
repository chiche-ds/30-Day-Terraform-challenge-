# Day 12: Zero-Downtime Deployment with Terraform

## Participant Details

- **Name:** Otu Michael Udo
- **Task Completed:** Implement zero-downtime infra deployment with terraform using the blue/green strategy. Also wrote a blog post on the blue/green deployment strategy.
- **Date and Time:** 18th December, 2024 | 7:07 PM 

Zero downtime deployments are crucial for maintaining the availability and performance of applications during updates. One effective approach is Blue-Green deployment, where you maintain two environments (Blue and Green) and switch traffic between them without any disruption.

 Key Steps I learned to achieve Zero Downtime Deployments:
 AMI Configuration: One of the first things to do is to ensure the Amazon Machine Image (AMI) is exposed as an input variable in variables.tf. This allows you to easily update the AMI for the Blue and Green environments without disrupting the system.
Load Balancer: Use an Application Load Balancer (ALB) to route traffic to the active environment, minimizing downtime.
Auto Scaling Groups: Configure separate Auto Scaling Groups for Blue and Green environments, allowing seamless scaling and management of traffic.
Blue-Green Switching: Deploy new versions to the inactive environment, test it, and switch the load balancer to route traffic to it once it’s verified.

This lifecycle rule ensures there is 
## Terraform Code 
```hcl

terraform {
  required_version = ">= 1.0.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# Define provider
provider "aws" {
  region = "us-east-1"
}

# Define Security Groups for ALB
resource "aws_security_group" "alb" {
  name = "bg-alb-sg"
}

# Security Group Rule to Allow Inbound HTTP Traffic
resource "aws_security_group_rule" "allow_http_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.alb.id

  from_port   = 80
  to_port     = 80
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

# Data Sources for VPC and Subnets
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Define Load Balancer
resource "aws_lb" "example" {
  name               = "blue-green-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = data.aws_subnets.default.ids
  enable_deletion_protection = false
}

# Define Target Groups for Blue and Green Environments
resource "aws_lb_target_group" "blue" {
  name     = "blue-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.default.id
}

resource "aws_lb_target_group" "green" {
  name     = "green-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.default.id
}

# Define Load Balancer Listener
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.example.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "forward"
    target_group_arn = var.environment == "blue" ? aws_lb_target_group.blue.arn : aws_lb_target_group.green.arn
  }
}

# Define Auto Scaling Group for Blue and Green
resource "aws_launch_configuration" "blue" {
  name          = "blue-launch-configuration"
  image_id      = var.ami_id
  instance_type = var.instance_type
  security_groups = [aws_security_group.alb.id]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_launch_configuration" "green" {
  name          = "green-launch-configuration"
  image_id      = var.ami_id
  instance_type = var.instance_type
  security_groups = [aws_security_group.alb.id]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "blue" {
  desired_capacity     = 2
  max_size             = 3
  min_size             = 1
  vpc_zone_identifier  = data.aws_subnets.default.ids
  launch_configuration = aws_launch_configuration.blue.id
  target_group_arns    = [aws_lb_target_group.blue.arn]

  health_check_type = "ELB"
  health_check_grace_period = 300
}

resource "aws_autoscaling_group" "green" {
  desired_capacity     = 2
  max_size             = 3
  min_size             = 1
  vpc_zone_identifier  = data.aws_subnets.default.ids
  launch_configuration = aws_launch_configuration.green.id
  target_group_arns    = [aws_lb_target_group.green.arn]

  health_check_type = "ELB"
  health_check_grace_period = 300
}

```