# Day 5: Scaling Infrastructure

## Participant Details
- **Name:** Eddie Chem
- **Task Completed:** All tasks for Day 5 apart from social media post. Learned about different blocks in Terraform, and how to automate the deployment of a load balancer for scaling a cluster of web servers to meet up with traffic demands.
- **Date and Time:** 8/21/2024

## Terraform Code - Deploying Scalable Infrastructure - Servers with ASG
```hcl
provider "aws" {
  region = "us-east-2"
}

resource "aws_launch_template" "terraform_instance" {
  image_id               = "ami-0fb653ca2d3203ac1"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.instance.id]

  user_data = base64encode(<<-EOF
  #!/bin/bash
  echo "Hello, World" > index.html
  nohup busybox httpd -f -p ${var.server_port} &
  EOF
  )

  # Required when using a launch configuration with an auto scaling group.
  lifecycle {
    create_before_destroy = true
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

variable "server_port" {
  description = "The port the server will use for HTTP requests"
  type        = number
  default     = 8080
}

resource "aws_autoscaling_group" "terraform_instance" {
  launch_template {
    id      = aws_launch_template.terraform_instance.id
    version = "$Latest"
  }

  vpc_zone_identifier = data.aws_subnets.default.ids
  target_group_arns   = [aws_lb_target_group.asg.arn]
  health_check_type   = "ELB"
  min_size            = 2
  max_size            = 10

  tag {
    key                 = "Name"
    value               = "terraform-asg-example"
    propagate_at_launch = true
  }
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_instances" "asg_instances" {
  filter {
    name   = "tag:name"
    values = ["terraform-asg-terraform_instance"]
  }
}

# Output Variables
output "public_ips" {
  value       = data.aws_instances.asg_instances.public_ips
  description = "Public IP addresses of the instances in the Auto Scaling Group"
}

output "private_ips" {
  value       = data.aws_instances.asg_instances.public_ips
  description = "Private IP addresses of the instances in the Auto Scaling Group"
}

output "alb_dns_name" {
  value       = aws_lb.example.dns_name
  description = "The domain name of the load balancer"
}
```
## Terraform Code - Deploying Scalable Infrastructure - Load Balancer Config.
```hcl
# Load Balancer Resource Block With Security Group ID
resource "aws_lb" "example" {
  name               = "terraform-asg-example"
  load_balancer_type = "application"
  subnets            = data.aws_subnets.default.ids
  security_groups    = [aws_security_group.alb.id]
}
# Listener Resource Block
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.example.arn
  port              = 80
  protocol          = "HTTP"

  # Error Page: Returns a simple 404 page error message
  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "Oops! Looks like you took a wrong turn. Maybe try Google Maps?"
      status_code  = 404
    }
  }
}
# Security Group Block
resource "aws_security_group" "alb" {
  name = "terraform-example-alb"
  # Allow inbound HTTP requests
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  # Allow all outbound requests
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
# Load Balancer Target Group Resource Block
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
#Listener Rule Block
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
```
## Architecture Diagram:

![Architecture Diagram](https://drive.google.com/uc?export=view&id=1SwMHlOzNLcHxPlus6bUh_gaV1ZAZJhTB)


