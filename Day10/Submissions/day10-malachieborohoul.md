# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** BOROHOUL Soguelni Malachie
- **Task Completed:** I learned how to implement loops to create dynamic infrastructure. I also refactored my existing infrastructure, published a blog post
- **Date and Time:** 9/01/2024 08:50 PM 

## Terraform Code 
In the previous code, a fixed Auto Scaling Group and Launch Configuration were created. I now use count to dynamically deploy the required number of EC2 instances. I also use for_each to iterate over a map of values, instead of writing multiple security group rules for each port or protocol. I used count with conditionals to decide whether to deploy certain resources based on a boolean variable.

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

  count = var.asg_count
  image_id        = "ami-0b0ea68c435eb488d"
  instance_type   = var.instance_type
  security_groups = [aws_security_group.instance.id]

  # Render the User Data script as a template
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
  count = var.asg_count

  launch_configuration = aws_launch_configuration.example.name
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
  # name = random_pet.sg_instance_name.id
  name = "${var.cluster_name}-instance"

  for_each = {
    "instance" = "${var.cluster_name}-instance"
    "alb" = "${var.cluster_name}-alb"
  }


  ingress {
    from_port   = local.http_port
    to_port     = local.http_port
    protocol    = local.tcp_protocol
    cidr_blocks = local.all_ips
  }
}



resource "aws_security_group_rule" "http" {
   for_each = {
    "allow_http_inbound"  = { type = "ingress", from_port = local.http_port, to_port = local.http_port }
    "allow_http_outbound" = { type = "egress", from_port = local.http_port, to_port = local.http_port }
  }
  type              = each.value.type
  security_group_id = aws_security_group.alb.id
  from_port         = local.http_port
  to_port           = local.http_port
  protocol          = local.tcp_protocol
  cidr_blocks       = local.all_ips
}




# Load Balancer Resources
resource "aws_lb" "example" {
  count = var.enable_lb ? 1 : 0
  name               = var.cluster_name
  load_balancer_type = "application"
  subnets            = data.aws_subnets.default.ids
  security_groups    = [aws_security_group.alb.id]
}

resource "aws_lb_listener" "http" {
  count = var.enable_lb ? 1 : 0
  load_balancer_arn = aws_lb.example.arn
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
  count = var.enable_lb ? 1 : 0
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

data "terraform_remote_state" "db" {
  backend = "s3"
  config = {
    # bucket = "terraform-bsm-my-state"
    # key    = "stage/data-stores/mysql/terraform.tfstate"

    bucket = var.db_remote_state_bucket
    key    = var.db_remote_state_key
    region = "us-east-2"
  }
}

output "asg_name" {
  value       = aws_autoscaling_group.example.name
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
```
## Architecture 
[Name](link to image in S3 bucket)

