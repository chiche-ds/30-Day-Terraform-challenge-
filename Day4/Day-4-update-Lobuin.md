# Day 4: Mastering Basic Infrastructure with Terraform

## Name: NGWA DIEUDONNE LONUIN 
## Task Completed

1. **Reading**: I have read Chapter 2 of "Terraform: Up & Running" by Yevgeniy Brikman.
   - Pages: 60 - 69.
2. **Udemy Videos**: 
   - I have rewatch Day 3 videos (Videos 11, 12, and 13).
   -  I have watched "Input Variables" (Video 14).
   -  I have watched "Local Variables" (Video 15). 
3. **Activity**: 
   -  I have deployed a configurable web server using Terraform.
   -  I have deployed a clustered web server using Terraform.
### Date Wednestday 28 August at 2:24 am


# Terraform Code for the Deployment of a configurable web Servers
```hcl
provider "aws" {
  region = "us-east-2"
}
resource "aws_instance" "terraform_instance" {
  ami                         = "ami-0fb653ca2d3203ac1"
  instance_type               = "t2.micro"
  vpc_security_group_ids      = [aws_security_group.instance.id]
  user_data                   = <<-EOF
 #!/bin/bash
 echo "Hello, World" > index.html
 nohup busybox httpd -f -p ${var.server_port} &
 EOF
  user_data_replace_on_change = true
  tags = {
    Name = "demo_web_server"
  }
}
resource "aws_security_group" "instance" {
  name = "terraform-example-instance"
  ingress {
    from_port   = var.server_port
    to_port     = var.server_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
variable "server_port" {
 description = "The port the server will use for HTTP requests"
 type = number
 default = 8080
}
output "public_ip" {
 value = aws_instance.terraform_instance.public_ip
 description = "The public IP address of the web server"
}
output "private_ip" {
 value = aws_instance.terraform_instance.private_ip
 description = "The private IP address of the web server"
}
```

# Terraform Code for the deploying of clustered Servers

```hcl
provider "aws" {
  region = "us-east-2"
}
resource "aws_launch_template" "terraform_instance" {
  image_id        = "ami-0fb653ca2d3203ac1"
  instance_type   = "t2.micro"
  vpc_security_group_ids  = [aws_security_group.instance.id]
  user_data       = base64encode(<<-EOF
 #!/bin/bash
 echo "Hello, World" > index.html
 nohup busybox httpd -f -p ${var.server_port} &
 EOF
 )
  # Required when using a launch configuration with an auto scaling group.
  lifecycle {
    create_before_destroy = true
  }
}
resource "aws_security_group" "instance" {
  name = "terraform-example-instance"
  ingress {
    from_port   = var.server_port
    to_port     = var.server_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
variable "server_port" {
  description = "The port the server will use for HTTP requests"
  type        = number
  default     = 8080
}
resource "aws_autoscaling_group" "terraform_instance" {
  launch_template {
    id      = aws_launch_template.terraform_instance.id
    version = "$Latest"
  }
  vpc_zone_identifier  = data.aws_subnets.default.ids
  min_size             = 2
  max_size             = 10
  tag {
    key                 = "name"
    value               = "terraform-asg-terraform_instance"
    propagate_at_launch = true
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
data "aws_instances" "asg_instances" {
  filter {
    name   = "tag:name"
    values = ["terraform-asg-terraform_instance"]
  }
}

output "public_ips" {
  value       = data.aws_instances.asg_instances.public_ips
  description = "Public IP addresses of the instances in the Auto Scaling Group"
}

output "private_ips" {
  value       = data.aws_instances.asg_instances.private_ips
  description = "Private IP addresses of the instances in the Auto Scaling Group"
}
```
   
