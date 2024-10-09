# Day4: Mastering Basic Infrastructure with Terraform

### Name: Ajibola Mubarak
### Task Completed: Day 4: Mastering Basic Infrastructure with Terraform
### Date: 10/09/24
### Time: 6:30pm

### Deployment of Configurable Web Server

I configured the webserver to deploy a webserver using a configuration which referenced the variable file where it was stated. Below is the resource block with the referenced configuration `var.server_port`

```hcl
# Deploy a configurable web server using Terraform.
variable "server_port" {
  description = "The port the server will use for HTTP requests"
  type        = number
  default     = 8080
}

resource "aws_security_group" "instance" {
  name = "terraform-example-instance"
  ingress {
    from_port = var.server_port
    to_port   = var.server_port
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# clustered webserver with the help of Autosacling group using Terraform.
resource "aws_launch_configuration" "example" {
  image_id        = "ami-0fb653ca2d3203ac1"
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.instance.id]
  user_data       = <<-EOF
 #!/bin/bash
 echo "Hello, World" > index.html
 nohup busybox httpd -f -p ${var.server_port} &
 EOF
  # Required when using a launch configuration with an autoscaling group.
  lifecycle {
    create_before_destroy = true
  }
}

# VPC
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_autoscaling_group" "example" {
  launch_configuration = aws_launch_configuration.example.name
  vpc_zone_identifier  = data.aws_subnets.default.ids
  min_size             = 2
  max_size             = 10
  tag {
    key                 = "Name"
    value               = "terraform-asg-example"
    propagate_at_launch = true
  }
}
