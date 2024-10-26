# Day 4: Mastering Basic Infrastructure with Terraform

## Participant Details
- **Name:** NGUEKAM YOSSA Gabin
- **Task Completed:** 
  - **Book:** Chapter 2 of "Terraform: Up & Running" by Yevgeniy (Jim) Brikman 
    - pages: 60 - 70
  - **Udemy:**
    - Rewatch Day 3 videos
    - "Input Variables"
    - "Local Variables"

- **Date and Time:** 26/08/2024 14:00

## Terraform code

```hcl
####################################################
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

#########################
# Main configuration file
#########################

# Configure the AWS Provider
provider "aws" {
  region = "eu-west-3"
}

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

# Define launch template for web servers of auto scaling group
resource "aws_launch_template" "webserver_asg_template" {
  name_prefix     = var.webserver_template_name_prefix
  image_id        = data.aws_ami.ubuntu.id
  instance_type   = var.Webserver_instance_type
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

  launch_template {
    id = aws_launch_template.webserver_asg_template.id
    version = aws_launch_template.webserver_asg_template.latest_version
  }

  # tag {
  #   key = "Name"
  #   value = "Web Server"
  #   propagate_at_launch = true
  # }
}

#####################
# Define some outputs
#####################

output "webserver_autoscaling_group" {
  value = aws_autoscaling_group.webserver_asg.name
}

output "webserver_port_listening" {
  value = var.webserver_port
}



```