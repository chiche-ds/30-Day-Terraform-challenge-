# Day 5: Scaling Infrastructure

## Participant Details
- **Name:** Franklin Afolabi
- **Task Completed:** All tasks for Day 5. Learned about data block, configuration block, module blok and output block in Terraform. Deployed a load balancer for scaling a cluster of web servers to meet up with traffic demands.
- **Date and Time:** August 27, 2024 1844hrs


## Terraform Code 
``` provider "aws" {
    region = "us-east-2"
}

# Define data sources
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
    filter {
      name = "vpc-id"
      values = [data.aws_vpc.default.id]
    }
}

# Use variable to store your port
variable "server_port" {
  description = "The port the server will use for HTTP requests"
  type = number
  default = 8080
}

# Create the security group to allow port 8080 from any IPv4 address
resource "aws_security_group" "instance" {
    name = "tf-sg"

    ingress {
        from_port = var.server_port
        to_port = var.server_port
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    } 
    
}

# Create the resource block for the webserver launch configuration and create a user data script the fires up when the server is launched
resource "aws_launch_configuration" "webserver" {
    image_id = "ami-0fb653ca2d3203ac1"
    instance_type = "t2.micro"
    security_groups = [aws_security_group.instance.id]

    user_data = <<-EOF
    #!/bin/bash
    echo "Hello, World. Welcome to the use of Terraform in deploying infrastructure" > index.html
    nohup busybox httpd -f -p ${var.server_port} &
    EOF

    lifecycle {
      create_before_destroy = true
    }
}

# Create the autoscaling group
resource "aws_autoscaling_group" "example" {
  launch_configuration = aws_launch_configuration.webserver.name
  vpc_zone_identifier = data.aws_subnets.default.ids

  target_group_arns = [aws_lb_target_group.webserver.arn]
  health_check_type = "ELB"

  min_size = 2
  max_size = 10

  tag {
    key = "Name"
    value = "tf-example"
    propagate_at_launch = true
  }
}

# Create the ALB
resource "aws_lb" "webserver" {
  name = "tf-example"
  load_balancer_type = "application"
  subnets = data.aws_subnets.default.ids
  security_groups = [aws_security_group.alb.id]
}

# Create the ALB listener
resource "aws_lb_listener" "webserver" {
  load_balancer_arn = aws_lb.webserver.arn
  port = 80
  protocol ="HTTP"

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body ="404: page not found"
      status_code = 404
    }
  }
}

# Create security group for load balancer
resource "aws_security_group" "alb" {
  name = "tf-example"

  # Allow inbound HTTP request
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outbound requests
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]   
  }
}

# Create target group for auto scaling group
resource "aws_lb_target_group" "webserver" {
  name = "tf-example"
  port =  var.server_port
  protocol = "HTTP"
  vpc_id = data.aws_vpc.default.id

  health_check {
    path = "/"
    protocol = "HTTP"
    matcher = "200"
    interval = 15
    timeout = 3
    healthy_threshold = 2
    unhealthy_threshold = 2
  }
}

## Create the ALB listener rules
resource "aws_lb_listener_rule" "asg" {
  listener_arn = aws_lb_listener.webserver.arn
  priority = 100

  condition {
    path_pattern {
      values = ["*"]
    }
  }
  action {
    type = "forward"
    target_group_arn = aws_lb_target_group.webserver.arn
  }
}

output "alb_dns_name" {
    value = aws_lb.webserver.dns_name
    description = "The domain name of the load balancer"
}
```