# Day 6: Understanding Terraform State

## Participant Details
- **Name:** NGUEKAM YOSSA Gabin
- **Task Completed:** 
  - **Book:** Complete Chapter 3 
    - pages: 81 - 113
  - **Udemy:**
    - "Benefits of Terraform State" (Video 47)
    - "Managing Terraform State" (Video 48)
    - "Remote State Storage" (Video 49)
    - "State Locking and Backend Authentication" (Video 50)


- **Date and Time:** 10/09/2024 16:45

## Terraform code S3 remote state

main.tf
```hcl
######################################
# AWS S3 bucket as terraform backends
######################################

# Define terraform versions and required providers 
####################################################
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "eu-west-3"
}

# S3 bucket for terraform remote state
#######################################

# Create S3 bucket
resource "aws_s3_bucket" "terraform_state" {
  bucket = "30days-tfchall-infra-aws-state"

  lifecycle {
    prevent_destroy = true
  }
}

# Enable bucket versioning
resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Enable server-side encryption 
resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Disable public access to bucket
resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.terraform_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Dynamo DB table to implement state lock
##########################################

resource "aws_dynamodb_table" "tf_state_lock" {
  name = "tf-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

outputs.tf
```hcl
#####################
# Define some outputs
#####################

output "TF_state_s3_bucket_arn" {
  value = aws_s3_bucket.terraform_state.arn
}

output "TF_state_lock_dynamodb_table_name" {
  value = aws_dynamodb_table.tf_state_lock.name
}
```

## Terraform code infra

versions.tf
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "30days-tfchall-infra-aws-state"
    key = "infra.tfstate"
    region = "eu-west-3"
    dynamodb_table = "tf-state-lock"
    encrypt = true
  }
}
```
variables.tf

```hcl
##################################################
# Define variables to allow configurable resources
##################################################

variable "webserver_port" {
  description = "TCP port that webserver listen to"
  type        = number
  default     = 8000
}

variable "webserver_name" {
  description = "Name of web server"
  type        = string
  default     = "Web Server"
}

variable "Webserver_instance_type" {
  description = "Instance type of webserver"
  type        = string
  default     = "t2.micro"
}

variable "webserver_template_name_prefix" {
  description = "prefix of launch template name"
  type        = string
  default     = "tmpl-ws-"
}

variable "webserver_asg_name_prefix" {
  description = "prefix of auto scaling group name"
  type        = string
  default     = "asg-ws-"
}

variable "webserver_lb_name" {
  description = "Name of aws application loadbalancer used in front of auto scaling group"
  type        = string
  default     = "lb-webserver"
}
```
main.tf

```hcl
#########################
# Main configuration file
#########################

# Configure the AWS Provider
provider "aws" {
  region = "eu-west-3"
}

# Datasources
####################################

# Fetch ubuntu image from aws
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

# Fetch default vpc
data "aws_vpc" "default" {
  default = true
}

# Fetch subnets of default vpc
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Security groups
####################################

# Define security group to allow traffic to our EC2 instance
resource "aws_security_group" "webserver_sg" {
  name        = "webserver_sg"
  description = "Allow traffic from and to the webserver"
}

resource "aws_vpc_security_group_ingress_rule" "allow_traffic_to_webserver" {
  security_group_id = aws_security_group.webserver_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = var.webserver_port
  ip_protocol       = "tcp"
  to_port           = var.webserver_port
}

resource "aws_vpc_security_group_ingress_rule" "allow_ssh" {
  security_group_id = aws_security_group.webserver_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4" {
  security_group_id = aws_security_group.webserver_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv6" {
  security_group_id = aws_security_group.webserver_sg.id
  cidr_ipv6         = "::/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}

# Define security group to allow inbound traffic to lb
resource "aws_security_group" "lb_webserver" {
  name        = "lb-webserver-sg"
  description = "allow inbound traffic to lb for webservers"
}

resource "aws_vpc_security_group_ingress_rule" "allow_traffic_to_lb" {
  security_group_id = aws_security_group.lb_webserver.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = var.webserver_port
  ip_protocol       = "tcp"
  to_port           = var.webserver_port
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4_lb" {
  security_group_id = aws_security_group.lb_webserver.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}


# Auto scaling group
####################################

# Define launch template for web servers of auto scaling group
resource "aws_launch_template" "webserver_asg_template" {
  name_prefix            = var.webserver_template_name_prefix
  image_id               = data.aws_ami.ubuntu.id
  instance_type          = var.Webserver_instance_type
  vpc_security_group_ids = [aws_security_group.webserver_sg.id]
  user_data = base64encode(<<-EOF
    #!/bin/bash

    # Install nginx
    apt-get update && sudo apt-get install -y nginx

    # Customize index.html and listening port
    echo "<h1>Message from host: $(hostname)</h1>" > /var/www/html/index.html
    echo "<h1>Succesfully deployed web server on AWS !</h1>" >> /var/www/html/index.html
    sed -i 's/listen 80/listen ${var.webserver_port}/' /etc/nginx/sites-enabled/default

    # restart nginx
    systemctl restart nginx
  EOF
  )

  tag_specifications {
    resource_type = "instance"
    tags = {
      server_type = "web"
      Name        = "Web server"
    }
  }
}

# Creates auto scaling group
resource "aws_autoscaling_group" "webserver_asg" {
  min_size            = 2
  desired_capacity    = 3
  max_size            = 6
  name_prefix         = var.webserver_asg_name_prefix
  vpc_zone_identifier = data.aws_subnets.default.ids
  health_check_type   = "ELB"
  target_group_arns   = [aws_lb_target_group.webserver.arn]


  launch_template {
    id      = aws_launch_template.webserver_asg_template.id
    version = aws_launch_template.webserver_asg_template.latest_version
  }

  # tag {
  #   key = "Name"
  #   value = "Web Server"
  #   propagate_at_launch = true
  # }
}

# Load balancer
####################################

# Define lb target group
resource "aws_lb_target_group" "webserver" {
  name        = "ASG-webserver-pool"
  port        = 8000
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = data.aws_vpc.default.id

  health_check {
    enabled             = true
    path                = "/"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 15
    timeout             = 3
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

# Define application load balancer
resource "aws_lb" "webserver_lb" {
  name               = var.webserver_lb_name
  internal           = false
  load_balancer_type = "application"
  subnets            = data.aws_subnets.default.ids
  security_groups    = [aws_security_group.lb_webserver.id]

  tags = {
    Name = "LB webserver"
  }
}

# Define listener 
resource "aws_lb_listener" "webserver_lb" {
  load_balancer_arn = aws_lb.webserver_lb.arn
  port              = "8000"
  protocol          = "HTTP"

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/html"
      message_body = "<h1> ERREUR: Page Non Trouvée !</h1>"
      status_code  = 404
    }
  }
}

# Addd listener rule
resource "aws_lb_listener_rule" "webserver_lb" {
  listener_arn = aws_lb_listener.webserver_lb.arn
  priority     = 100

  condition {
    path_pattern {
      values = ["/"]
    }
  }

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.webserver.arn
  }
}

```
outputs.tf
```hcl
#####################
# Define some outputs
#####################

output "lb_dns_name" {
  value = aws_lb.webserver_lb.dns_name
}

output "webserver_port_listening" {
  value = var.webserver_port
}
```

## Architecture

[Scaled infrastructure with aws](https://github.com/iNgk42/aws_architecture_diagrams/blob/main/terraform-s3-remote-state.drawio.png?raw=true)