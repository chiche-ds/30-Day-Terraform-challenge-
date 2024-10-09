# Day 8: Reusing Infrastructure with Modules

## Participant Details
- **Name:** Franklin Afolabi
- **Task Completed:** Worked on modules and saw the benefits of reusable modules and how it compares to root modules
- **Date and Time:** September 6 0454hrs

### Modules
```

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

data "terraform_remote_state" "db" {
  backend = "s3"

  config = {
    bucket = "var.db_remote_state_bucket"
    key = "var.db_remote_state_key"
    region = "us-east-2"
  }
}


locals {
  http_port = 80
  any_port = 0
  any_protocol = "-1"
  tcp_protocol = "tcp"
  all_ips = ["0.0.0.0/0"]

}


# Create the security group to allow port 8080 from any IPv4 address
resource "aws_security_group" "instance" {
    name = "${var.cluster_name}-instance"

    ingress {
        from_port = var.server_port
        to_port = var.server_port
        protocol = local.tcp_protocol
        cidr_blocks = local.all_ips
    }

}

# Create the resource block for the webserver launch configuration
# Create a user data script the fires up when the server is launched
resource "aws_launch_configuration" "webserver" {
    image_id = "ami-0fb653ca2d3203ac1"
    instance_type = var.instance_type
    security_groups = [aws_security_group.instance.id]

    # Render the user data script as a template
    user_data = templatefile("${path.module}/user-data.sh", {
      server_port = var.server_port
      db_address = data.terraform_remote_state.db.outputs.address
      db_port = data.terraform_remote_state.db.outputs.port

    })

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

  min_size = var.min_size
  max_size = var.max_size

  tag {
    key = "Name"
    value = var.cluster_name
    propagate_at_launch = true
  }
}

# Create the ALB
resource "aws_lb" "webserver" {
  name = "${var.cluster_name}-alb-webserver"
  load_balancer_type = "application"
  subnets = data.aws_subnets.default.ids
  security_groups = [aws_security_group.alb.id]
}

# Create the AWS listener
resource "aws_lb_listener" "webserver" {
  load_balancer_arn = aws_lb.webserver.arn
  port = local.http_port
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
  name = "${var.cluster_name}-alb"
}

resource "aws_security_group_rule" "allow_http_inbound" {
  type = "ingress"
  security_group_id = aws_security_group.alb.id

    from_port = local.http_port
    to_port = local.http_port
    protocol = local.tcp_protocol
    cidr_blocks = local.all_ips
  }

resource "aws_security_group_rule" "allow_all_outbound" {
  type =  "egress"
  security_group_id = aws_security_group.alb.id
    from_port = local.any_port
    to_port = local.any_port
    protocol = local.any_protocol
    cidr_blocks = local.all_ips
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

# Create the ALB listerner rules
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

```
