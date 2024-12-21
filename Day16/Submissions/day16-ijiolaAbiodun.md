# Load remote state for the database
data "terraform_remote_state" "db" {
  backend = "s3"

  config = {
    bucket = "my-tf-s3-bucket-${random_id.randomness.hex}"
    key    = "path/to/db/terraform.tfstate"
    region = "us-east-1"
  }
}

# Generate a random ID (used in bucket name or other resources)
resource "random_id" "randomness" {
  byte_length = 8
}

# Create a VPC
resource "aws_vpc" "hello_world_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "hello-world-vpc"
  }
}

# Create subnets
resource "aws_subnet" "hello_world_subnet" {
  count             = length(var.subnet_cidrs)
  vpc_id            = aws_vpc.hello_world_vpc.id
  cidr_block        = var.subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name = "hello-world-subnet-${count.index}"
  }
}

# Security group
resource "aws_security_group" "instance" {
  name_prefix = "hello-world-sg"
  vpc_id      = aws_vpc.hello_world_vpc.id

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

  tags = {
    Name = "hello-world-sg"
  }
}

# Create an ALB Target Group
resource "aws_lb_target_group" "asg" {
  name        = "hello-world-${var.environment}"
  port        = var.server_port
  protocol    = "HTTP"
  vpc_id      = aws_vpc.hello_world_vpc.id
  target_type = "instance"

  health_check {
    path                = "/"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 15
    timeout             = 3
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }

  tags = {
    Name = "hello-world-tg"
  }
}

# Create ALB Listener Rule
resource "aws_lb_listener_rule" "asg" {
  listener_arn = module.alb_http_listener_arn
  priority     = 100

  conditions {
    field  = "path-pattern"
    values = ["*"]
  }

  actions {
    type             = "forward"
    target_group_arn = aws_lb_target_group.asg.arn
  }

  tags = {
    Name = "hello-world-listener-rule"
  }
}

# Create Launch Configuration
resource "aws_launch_configuration" "work" {
  image_id        = var.ami
  instance_type   = var.instance_type
  security_groups = [aws_security_group.instance.id]
  user_data       = templatefile("${path.module}/user-data.sh", {
    server_port  = var.server_port
    db_address   = data.terraform_remote_state.db.outputs.db_address
    db_port      = data.terraform_remote_state.db.outputs.port
    server_text  = var.server_text
  })

  lifecycle {
    create_before_destroy = true
  }
}

module "asg" {
  source = "../../cluster/asg-rolling-deploy"

  cluster_name      = "hello-world-${var.environment}"
  ami               = var.ami
  instance_type     = var.instance_type
  user_data         = templatefile("${path.module}/user-data.sh", {
    server_port = var.server_port
    db_address  = data.terraform_remote_state.db.outputs.db_address
    db_port     = data.terraform_remote_state.db.outputs.port
    server_text = var.server_text
  })
  min_size          = var.min_size
  max_size          = var.max_size
  enable_autoscaling = var.enable_autoscaling

  subnet_ids        = data.aws_subnet.default.ids
  target_group_arns = [aws_lb_target_group.asg.arn]
  health_check_type = "ELB"

  custom_tags = var.custom.custom_tags
}

module "alb" {
  source = "../../networking/alb"

  alb_name   = "hello-world-${var.environment}"
  subnet_ids = data.aws_subnet.default.ids
}

output "alb_dns_name" {
  value       = module.alb.alb_dns_name
  description = "The domain name of the load balancer"
}

output "asg_name" {
  value       = module.asg.asg_name
  description = "The name of the Auto Scaling Group"
}

output "instance_security_group_id" {
  value       = module.asg.instance_security_group_id
  description = "The ID of the EC2 Instance Security Group"
}

