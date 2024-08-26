# Day5: Scaling Infrastructure

## Participant Details
- **Name:** Adaeze Nnamdi-Udekwe
- **Task Completed:**  I created an application load balancer to route traffic to healthy servers I created. I also made social media posts
- **Date and Time:** 8/22/2024 4:53 PM

### This is the `main.tf` with all the configurations  
```hcl
provider "aws" {
  region = "us-east-1"
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


```hcl
output "alb_dns_name" {
value = aws_lb.example.dns_name
description = "The domain name of the load balancer"
}
resource "aws_launch_configuration" "example" {
  image_id        = "ami-04a81a99f5ec58529"
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.instance.id]
  user_data = <<-EOF
#!/bin/bash
echo "Hi! Adaeze here. I am learning more on terraform. Join me on this journey!" > index.html
nohup busybox httpd -f -p ${var.server_port} &
EOF

  # Required when using a launch configuration with an auto scaling group.
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "example" {
  launch_configuration = aws_launch_configuration.example.name
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

resource "aws_security_group" "instance" {
  name = "terraform-example-instance"
  ingress {
    from_port   = var.server_port
    to_port     = var.server_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.example.arn
  port              = 80
  protocol          = "HTTP"

  # By default, return a simple 404 page
  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "404: page not found"
      status_code  = 404
    }
  }
}

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

resource "aws_lb" "example" {
  name               = "terraform-asg-example"
  load_balancer_type = "application"
  subnets            = data.aws_subnets.default.ids
  security_groups    = [aws_security_group.alb.id]
}

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
### This is the `output.tf` file where I get the ALB DNS name url instead of an IP address.

```hcl
output "alb_dns_name" {
value = aws_lb.example.dns_name
description = "The domain name of the load balancer"
}
```
### The `variable.tf` is where I put in the variables for when they can be adjusted and reusable

```hcl
variable "server_port" {
description = "The port the server will use for HTTP requests"
type = number
default = 8080
}
