
# Day5: Scaling Infrastructure

## Participant Details
- **Name:** EJIBODE IBRAHEEM
- **Task Completed:**  I created an application load balancer to route traffic to healthy servers I created. I also made social media posts
- **Date and Time:** 5/12/2024 9:52 PM


```
provider "aws" {
  region ="us-east-2"
}

# declaring a variable for port 8080
variable "server_port" {
 description = "The port the server will use for HTTP requests"
 type = number
 default= 8080
}

# creating  EC2 instance

resource "aws_instance" "my_instance" {
    ami ="ami-0fb653ca2d3203ac1"
    instance_type = "t2.micro"
    vpc_security_group_ids = [aws_security_group.instance_sg.id]
    user_data = <<-EOF
 #!/bin/bash
 echo "Hello, World" > index.html
 nohup busybox httpd -f -p ${var.server_port} &
 EOF
 

 user_data_replace_on_change = true
    
    tags = {
      Name = "terraform-example"
    }
  
}

# creating  security group
resource "aws_security_group" "instance_sg" {
 name = "terraform-example-instance"
 ingress {
 from_port = var.server_port
 to_port = var.server_port
 protocol = "tcp"
 cidr_blocks = ["0.0.0.0/0"]
 }
}


# creating launch configuration for ASG

resource "aws_launch_configuration" "example" {
 image_id = "ami-0fb653ca2d3203ac1"
 instance_type = "t2.micro"
 security_groups = [aws_security_group.instance_sg.id]
 user_data = <<-EOF
 #!/bin/bash
 echo "Hello, World" > index.html
 nohup busybox httpd -f -p ${var.server_port} &
 EOF
 # Required when using a launch configuration with an auto scaling group.
 lifecycle {
 create_before_destroy = true
 }
}

# creating autoscalling group
resource "aws_autoscaling_group" "example" {
 launch_configuration = aws_launch_configuration.example.name
 vpc_zone_identifier = data.aws_subnets.default.ids
 target_group_arns = [aws_lb_target_group.asg.arn]
 health_check_type = "ELB"
 min_size = 2
 max_size = 10
 tag {
 key = "Name"
 value = "terraform-asg-example"
 propagate_at_launch = true
 }
}




data "aws_vpc" "default" {
 default = true
}

data "aws_subnets" "default" {
 filter {
 name = "vpc-id"
 values = [data.aws_vpc.default.id]
 }
}

# creating ALB resource
resource "aws_lb" "example" {
 name = "terraform-asg-example"
 load_balancer_type = "application"
 subnets = data.aws_subnets.default.ids
 
}
# creatin the listener
resource "aws_lb_listener" "http" {
 load_balancer_arn = aws_lb.example.arn
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
 name = "terraform-example-alb"
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


# creating a target bgroup for your ASG
resource "aws_lb_target_group" "asg" {
 name = "terraform-asg-example"
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


# Creating listenr rule
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
 target_group_arn = aws_lb_target_group.asg.arn
 }
}


output "alb_dns_name" {
 value = aws_lb.example.dns_name
 description = "The domain name of the load balancer"
}
```