# Day 11: Terraform Conditionals

## Participant Details

- **Name:** BOROHOUL Soguelni Malachie
- **Task Completed:** I completed the chapters and understood how to implement conditionals. I also refactored my existing infrastructure.
- **Date and Time:** 9/01/2024 09:50 PM 

## Terraform Code 
I created variables like: `deploy_resources` a flag to enable or disable the deployment of resources, `enable_lb` which is a flag to enable Load Balancer.
In EC2 Launch Configuration & Auto Scaling Group i implemented a conditional based on `deploy_resources`. Security Groups and Load Balancer there are rules based on `deploy_resources` and `enable_lb`

### modules/services/webserver-cluster/main.tf
```hcl

# Data Sources
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Random Pet Resources
resource "random_pet" "sg_instance_name" {
  prefix = "terraform-example-instance"
  length = 2
}

resource "random_pet" "sg_alb_name" {
  prefix = "terraform-example-alb"
  length = 2
}

resource "random_pet" "lb_name" {
  prefix = "terraform-asg"
  length = 2
}

resource "random_pet" "tg_name" {
  prefix = "terraform-asg"
  length = 2
}

# EC2 and Auto Scaling Resources
resource "aws_launch_configuration" "example" {
  count = var.deploy_resources ? var.asg_count : 0

  image_id        = "ami-0b0ea68c435eb488d"
  instance_type   = var.instance_type
  security_groups = [aws_security_group.instance.id]

  user_data = templatefile("${path.module}/user-data.sh", {
    server_port = var.server_port
    db_address  = data.terraform_remote_state.db.outputs.address
    db_port     = data.terraform_remote_state.db.outputs.port
  })

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "example" {
  count = var.deploy_resources ? var.asg_count : 0

  launch_configuration = aws_launch_configuration.example[0].name
  vpc_zone_identifier  = data.aws_subnets.default.ids
  target_group_arns    = [aws_lb_target_group.asg.arn]
  health_check_type    = "ELB"
  min_size             = var.min_size
  max_size             = var.max_size

  tag {
    key                 = "Name"
    value               = var.cluster_name
    propagate_at_launch = true
  }
}

# Security Group Resources
resource "aws_security_group" "instance" {
  count = var.deploy_resources ? 1 : 0
  name  = "${var.cluster_name}-instance"

  ingress {
    from_port   = local.http_port
    to_port     = local.http_port
    protocol    = local.tcp_protocol
    cidr_blocks = local.all_ips
  }
}

resource "aws_security_group" "alb" {
  count = var.deploy_resources && var.enable_lb ? 1 : 0
  name  = "${var.cluster_name}-alb"

  ingress {
    from_port   = local.http_port
    to_port     = local.http_port
    protocol    = local.tcp_protocol
    cidr_blocks = local.all_ips
  }
}

resource "aws_security_group_rule" "http" {
  count = var.deploy_resources && var.enable_lb ? 2 : 0

  type              = each.key == "allow_http_inbound" ? "ingress" : "egress"
  security_group_id = aws_security_group.alb.id
  from_port         = local.http_port
  to_port           = local.http_port
  protocol          = local.tcp_protocol
  cidr_blocks       = local.all_ips
}

# Load Balancer Resources
resource "aws_lb" "example" {
  count = var.deploy_resources && var.enable_lb ? 1 : 0

  name               = var.cluster_name
  load_balancer_type = "application"
  subnets            = data.aws_subnets.default.ids
  security_groups    = [aws_security_group.alb.id]
}

resource "aws_lb_listener" "http" {
  count = var.deploy_resources && var.enable_lb ? 1 : 0

  load_balancer_arn = aws_lb.example[0].arn
  port              = local.http_port
  protocol          = "HTTP"

  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "404: page not found"
      status_code  = 404
    }
  }
}

resource "aws_lb_target_group" "asg" {
  count = var.deploy_resources && var.enable_lb ? 1 : 0

  name     = random_pet.tg_name.id
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
  count = var.deploy_resources && var.enable_lb ? 1 : 0

  listener_arn = aws_lb_listener.http[0].arn
  priority     = 100

  condition {
    path_pattern {
      values = ["*"]
    }
  }

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.asg[0].arn
  }
}

data "terraform_remote_state" "db" {
  backend = "s3"
  config = {
    bucket = var.db_remote_state_bucket
    key    = var.db_remote_state_key
    region = "us-east-2"
  }
}

output "asg_name" {
  value       = aws_autoscaling_group.example[0].name
  description = "The name of the Auto Scaling Group"
}


```

### modules/services/webserver-cluster/variables.tf
```hcl


# Variables
variable "server_port" {
  type        = number
  default     = 8080
  description = "The port the server will use for HTTP requests"
}

variable "cluster_name" {
  description = "The name to use for all the cluster resources"
  type        = string
}

variable "db_remote_state_bucket" {
  description = "The name of the S3 bucket for the database's remote state"
  type        = string
}

variable "db_remote_state_key" {
  description = "The path for the database's remote state in S3"
  type        = string
}


variable "instance_type" {
  description = "The type of EC2 Instances to run (e.g. t2.micro)"
  type        = string
}

variable "min_size" {
  description = "The minimum number of EC2 Instances in the ASG"
  type        = number
}


variable "max_size" {
  description = "The maximum number of EC2 Instances in the ASG"
  type        = number
}


locals {
  http_port    = 80
  any_port     = 0
  any_protocol = "-1"
  tcp_protocol = "tcp"
  all_ips      = ["0.0.0.0/0"]
}


variable "asg_count" {
  description = "Number of Auto Scaling Groups to create"
  type        = number
  default     = 1
}

variable "enable_lb" {
  description = "Set to true to deploy Load Balancer"
  type        = bool
  default     = true
}


variable "deploy_resources" {
  description = "Flag to determine if resources should be deployed"
  type        = bool
  default     = true
}

variable "region" {
  description = "AWS region where resources will be deployed"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment (e.g., dev, prod)"
  type        = string
  default     = "dev"
}

```
## Architecture 
[Name](link to image in S3 bucket)

