# Scailing my webserver cluster

```hcl
}
resource "aws_autoscaling_group" "Terraform_ASG" {
  launch_template {
    id      = aws_launch_template.instance.id
    version = "$Latest"
  }
  vpc_zone_identifier  = data.aws_subnets.default.ids
  min_size             = 2
  max_size             = 10
  tag {
    key                 = "name"
    value               = "Terraform-ASG-Terraform_Instance"
    propagate_at_launch = true
  }
}

```
# Deploy a load balancer

```hcl
resource "aws_lb" "Terraform_ALB" {
name = "Terraform-ASG"
load_balancer_type = "application"
subnets = data.aws_subnets.default.ids
}
resource "aws_lb_listener" "http" {
load_balancer_arn = "Create n add loadbalancer arn "
port = 80
protocol = "HTTP"
# By default, return a simple 404 page
default_action {
type = "fixed-response"
fixed_response {
content_type = "text/plain"
message_body = "404: page not found"
status_code = 404
}
}
}
resource "aws_security_group" "alb" {
name = "Terraform_ALB"
# Allow inbound HTTP requests
ingress {
from_port = 80
to_port = 80
protocol = "tcp"
cidr_blocks = ["0.0.0.0/0"]
}
# Allow all outbound requests
egress {
from_port = 0
to_port = 0
protocol = "-1"
cidr_blocks = ["0.0.0.0/0"]
}
}

# Create a target group for the Auto Scaling Group
resource "aws_lb_target_group" "Terraform-ASG-Target-Group" {
name = "Terrraform-ASG"
port = var.server_port
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
resource "aws_lb_listener_rule" "asg" {
listener_arn = aws_lb_listener.http.arn
priority = 100
condition {
path_pattern {
values = ["*"]
}
}
action {
type = "forward"
target_group_arn = aws_lb_target_group.Terraform-ASG-Target-Group.arn
}
}
# DNS name of the load balancer
output "alb_dns_name" {
value = "Creat n add loadbalancer arn"
description = "The domain name of the load balancer"
}

