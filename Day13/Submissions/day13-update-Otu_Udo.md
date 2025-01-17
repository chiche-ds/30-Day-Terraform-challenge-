# Day 13: Managing Sensitive Data in Terraform

## Participant Details

- **Name:** Otu Michael Udo
- **Task Completed:** 
- **Date and Time:** 19th December, 2024 | 5:00 PM

Today, I used AWS Secrets Manager to securely manage secrets for the web server I created, preventing risks such as data breaches or unauthorized access.
🔐 Encryption: AWS Secrets Manager automatically encrypts secrets with AWS KMS, ensuring data protection at rest.
🔑 Access Control: Fine-grained IAM policies allow you to control who can access and manage secrets.
🔄 Automated Rotation: Secrets can be automatically rotated, improving security by reducing the risk of stale credentials.
🛡️ Secure Access: Secrets are retrieved securely, reducing the need to hardcode sensitive information in code.

To securely handle sensitive values like passwords in Terraform, you can use the variable.tf file to define a variable and prompt the user for input instead of hardcoding the value in your main.tf. This ensures the password isn’t exposed in your configuration files.
I learnt how to encrpty sensitive data inside the terraform state file.
I also learnt how secrets can be created in various cloud providers and imported into terraform.

## Terraform Code 
main.tf
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
variable.tf
```hcl
variable "ec2_admin_password" {
  description = "The admin password for the EC2 instance"
  type        = string
  sensitive   = true
}

``