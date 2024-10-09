# Day 7: Understanding Terraform State Part 2

## Participant Details
- **Name:** Sunil Kumar
- **Task Completed:** :  File Layout and Workspace Layout 
- **Date and Time:** 2024-09-16 7:36pm


### Practice using Workspace Layout/File Layout to manage to terraform State
#### main.tf
```hcl
provider "aws" {
region = "ap-south-1"
}

#statefile isolation
resource "aws_instance" "exampleday7" {
ami = "ami-0522ab6e1ddcc7055"
instance_type = "t2.micro"
}
resource "aws_launch_configuration" "example" {
image_id = "ami-0522ab6e1ddcc7055"
instance_type = "t2.micro"
security_groups = [aws_security_group.instance.id]
# Render the User Data script as a template
user_data = templatefile("user-data.sh", {
server_port = var.server_port
db_address = data.terraform_remote_state.db.outputs.address
db_port = data.terraform_remote_state.db.outputs.port
})
# Required when using a launch configuration with an auto scaling group.
lifecycle {
create_before_destroy = true
}
}
data "terraform_remote_state" "db" {
backend = "s3"
config = {
bucket = "sunil-day7-mybucket"
key = "stage/data-stores/mysql/terraform.tfstate"
region = "ap-south-1"
}
}

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

resource "aws_security_group" "instance" {
  name = var.instance_security_group_name

  ingress {
    from_port   = var.server_port
    to_port     = var.server_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "example" {
  name               = var.alb_name
  load_balancer_type = "application"
  subnets            = data.aws_subnets.default.ids
  security_groups    = [aws_security_group.alb7.id]
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

resource "aws_security_group" "alb7" {
  name = var.alb_security_group_name

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

data "terraform_remote_state" "db7" {
  backend = "s3"

  config = {
    bucket = var.db_remote_state_bucket
    key    = var.db_remote_state_key
    region = "ap-south-1"
  }
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
```

#### RDS database and backend.hcl
```hcl
provider "aws" {
region = "ap-south-1"
}

resource "aws_db_instance" "dbday7" {
identifier_prefix = "terraform-up-and-running"
engine = "mysql"
allocated_storage = 20
instance_class = "db.t3.micro"
skip_final_snapshot = true
db_name = "example_database"
username = var.db_username
password = var.db_password
}

terraform {
backend "s3" {
# Replace this with your bucket name!
bucket = "sunil-day7-mybucket"
key = "stage/data-stores/mysql/terraform.tfstate"
//key= "stage1/data-stores1/mysql1/terraform.tfstate"
region = "ap-south-1"
# Replace this with your DynamoDB table name!
dynamodb_table = "sunil-day7-mytable"
encrypt = true
}
}

```


