## Deploying a Highly Available Web App on AWS Using Terraform in a file `main.tf` 

```hcl
provider "aws" {
  region = "us-east-2"
}
```

step 1.1 
Creating an aws_launch_configuration launch configuration which specifies how to configure each EC2 Instance in the ASG.
--doesn’t support tags
-- lifecycle :: ensures the resource is created before destroyed as it is referenced else by aws_autoscaling_group


```hcl
resource "aws_launch_configuration" "example" {
  image_id        = "ami-0fb653ca2d3203ac1"
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.instance.id]

  user_data = <<-EOF
              #!/bin/bash
              echo "Hello, World" > index.html
              nohup busybox httpd -f -p ${var.server_port} &
              EOF
  lifecycle {
    create_before_destroy = true
  }
}
```

step 1.2 create the ASG itself using the aws_autoscaling_group resource:

```hcl
resource "aws_autoscaling_group" "example" {
  launch_configuration = aws_launch_configuration.example.name
  vpc_zone_identifier  = data.aws_subnets.default.ids

  target_group_arns = [aws_lb_target_group.asg.arn]
  health_check_type = "ELB"

  min_size = 2
  max_size = 10

  tag {
    key                 = "Name"
    value               = "terraform-asg-example"
    propagate_at_launch = true
  }
}

```
--A data source represents a piece of read-only information that is fetched from the
//provider (in this case, AWS) every time you run Terraform

```hcl
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}
```
step 2.1 deploying a Load Balancer
```hcl
resource "aws_lb" "example" {
  name               = var.alb_name
  load_balancer_type = "application"
  subnets            = data.aws_subnets.default.ids
  security_groups    = [aws_security_group.alb.id]
}
```
step 2.2
A listener is a process that checks for connection requests, using the protocol and port

```hcl
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
```
step 2.3 the security group our network lb will use.
```hcl
resource "aws_security_group" "alb" {
  name = "terraform-example-alb"
  ingress {
    from_port   = var.server_port
    to_port     = var.server_port
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
step 2.4 
target group will health check your Instances by periodically sending an HTTP
request to each Instance and will consider the Instance “healthy” only if the Instance
returns a response that matches the configured matcher
```hcl
resource "aws_lb_target_group" "asg" {
  name     = var.alb_name
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
```
step 2.5
 --listener rule:
```hcl
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

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1pahmo1a0inr2odvhz1x.png)

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9totvpmexm6e41705ce6.png)

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/02waqcn4kcqdm6fslmzr.png)

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0cwyott9fdtlw8h4o7ow.png)

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gq1rak275sbpm1sdgv10.png)
