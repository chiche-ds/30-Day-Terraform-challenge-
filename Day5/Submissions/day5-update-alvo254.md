# Day 5: Scaling Infrastructure

## Participant Details
- **Name:** Alvin Ndungu
- **Task Completed:** Scaling Infrastructure
- **Date and Time:** 2024-08-19 14:51pm

```
terraform {
  required_providers {
    aws = {

      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_vpc" "webserver-vpc" {
  instance_tenancy                 = "default"
  cidr_block                       = "172.16.0.0/20"
  assign_generated_ipv6_cidr_block = true
  enable_dns_hostnames             = true

  tags = {
    Name = "webserver-vpc"
  }
}

data "aws_availability_zones" "available_zones" {}

resource "aws_subnet" "public_subnet1" {
  vpc_id                          = aws_vpc.webserver-vpc.id
  cidr_block                      = "172.16.0.0/22"
  map_public_ip_on_launch         = true
  availability_zone               = data.aws_availability_zones.available_zones.names[0]

  tags = {
    Name = "webserver-public-sb-1"
  }
}

resource "aws_subnet" "public_subnet2" {
  vpc_id                          = aws_vpc.webserver-vpc.id
  cidr_block                      = "172.16.4.0/22"
  map_public_ip_on_launch         = true
  availability_zone               = data.aws_availability_zones.available_zones.names[1]

  tags = {
    Name = "webserver-public-sb-2"
  }
}

resource "aws_internet_gateway" "web" {
  vpc_id = aws_vpc.webserver-vpc.id

  tags = {
    Name = "webserver-igw"
  }
}

resource "aws_route_table" "web-rtb" {
  vpc_id = aws_vpc.webserver-vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.web.id
  }

  tags = {
    Name = "webserver-public-rt"
  }
}

resource "aws_launch_configuration" "web_launch_config" {
  image_id          = "ami-04a81a99f5ec58529"
  instance_type     = "t2.micro"
  security_groups   = [aws_security_group.web_sg.id]
  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install -y nginx
              sudo systemctl start nginx
              sudo systemctl enable nginx
              EOF
}

resource "aws_autoscaling_group" "web_asg" {
  vpc_zone_identifier = [aws_subnet.public_subnet1.id, aws_subnet.public_subnet2.id]
  desired_capacity    = 2
  max_size            = 3
  min_size            = 1
  launch_configuration = aws_launch_configuration.web_launch_config.id

  tag {
    key                 = "Name"
    value               = "web-server"
    propagate_at_launch = true
  }

  health_check_type         = "EC2"
  health_check_grace_period = 300

  target_group_arns = [aws_lb_target_group.web_target_group.arn]
}

resource "aws_security_group" "web_sg" {
  vpc_id      = aws_vpc.webserver-vpc.id
  name        = "web-sg"
  description = "Allow HTTP and SSH traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
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

resource "aws_lb" "web_alb" {
  name               = "web-cluster-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web_sg.id]
  subnets            = [aws_subnet.public_subnet1.id, aws_subnet.public_subnet2.id]

  tags = {
    Name = "web-cluster-alb"
  }
}

resource "aws_lb_target_group" "web_target_group" {
  name     = "web-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.webserver-vpc.id

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    interval            = 30
    path                = "/"
    matcher             = "200"
  }

  tags = {
    Name = "web-target-group"
  }
}

resource "aws_lb_listener" "web_alb_listener" {
  load_balancer_arn = aws_lb.web_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web_target_group.arn
  }
}

```