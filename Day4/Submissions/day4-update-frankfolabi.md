# Day 4: Mastering Basic Infrastructure with Terraform

## Participant Details
- **Name:** Franklin Afolabi
- **Task Completed:** Completed pages 60 - 69 of Chapter 2 in "Terraform: Up & Running", watched the required Udemy videos to reinforce the learning, set up a configurable and clustered web servers using Terraform. I also explored the Terraform documentation to become more familar with the syntax.
- **Date and Time:** August 26, 2024 2115hrs

## Terraform code

```provider "aws" {
    region = "us-east-2"
}

# Define data sources
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
    filter {
      name = "vpc-id"
      values = [data.aws_vpc.default.id]
    }
}

# Use variable to store your port
variable "server_port" {
  description = "The port the server will use for HTTP requests"
  type = number
  default = 8080
}

# Create the security group to allow port 8080 from any IPv4 address
resource "aws_security_group" "instance" {
    name = "tf-sg"

    ingress {
        from_port = var.server_port
        to_port = var.server_port
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    } 
    
}

# Create the resource block for the webserver launch configuration and create a user data script the fires up when the server is launched
resource "aws_launch_configuration" "webserver" {
    image_id = "ami-0fb653ca2d3203ac1"
    instance_type = "t2.micro"
    security_groups = [aws_security_group.instance.id]

    user_data = <<-EOF
    #!/bin/bash
    echo "Hello, World. Welcome to the use of Terraform in deploying infrastructure" > index.html
    nohup busybox httpd -f -p ${var.server_port} &
    EOF

    lifecycle {
      create_before_destroy = true
    }
}

# Create the autoscaling group
resource "aws_autoscaling_group" "example" {
  launch_configuration = aws_launch_configuration.webserver.name
  vpc_zone_identifier = data.aws_subnets.default.ids

  target_group_arns = [aws_lb_target_group.webserver.arn]
  health_check_type = "ELB"

  min_size = 2
  max_size = 10

  tag {
    key = "Name"
    value = "tf-example"
    propagate_at_launch = true
  }
}
```
