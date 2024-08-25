# Day4: Mastering Basic Infrastructure with Terraform

## Participant Details
- **Name:** gus
- **Task Completed:** 
-Deploy Configurable Web Server.
-Deploy Clustered Web Server.
-Chapter: Chapter 2 of "Terraform.
-Update the daily-update.md file.
- **Date and Time:** 8/22/2024 8:32 PM

 # Terraform Code - Deploying a Configurable Web Server
```hcl
provider "aws" {
  region  = "us-west-1"
  profile = "dev-profile"
}

resource "aws_instance" "Terraform_Instance_AMI1" {
  ami           = "ami-0e64c0b934d72ced5"
  instance_type = "t2.micro"

  tags = {
    Name = "Terraform Instance AMI1"
  }
}

resource "aws_instance" "Terraform_Instance_AMI2" {
  ami           = "ami-0e64c0b934d72ced5"
  instance_type = "t2.micro"

  user_data = <<-EOF
    #!/bin/bash
    echo "Hello, World" > index.html
    nohup busybox httpd -f -p 8080 &
  EOF

  user_data_replace_on_change = true

  tags = {
    Name = "Terraform Instance AMI2"
  }
}

resource "aws_security_group" "web_server1" {
  name = "Terraform Instance Security Group"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_security_group" "web_server2" {
  name = "Terraform Instance Securrity Group"
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
 value = aws_instance.Terraform_Instance_AMI2
 description = "The public IP address of the web server"
}
output "private_ip" {
 value = aws_instance.Terraform_Instance_AMI2
 description = "The private IP address of the web server"
}

```
# Terraform Code - Deploying Clustered Servers
```

resource "aws_launch_template" "instance" {
  image_id        = "ami-0e64c0b934d72ced5"
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
  name = "instance"
  ingress {
    from_port   = var.server_port
    to_port     = var.server_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_autoscaling_group" "Terraform_ASG" {
  launch_template {
    id      = aws_launch_template.instance.id
    version = "$Latest"
  }
  vpc_zone_identifier  = data.aws_subnets.default.ids
  min_size             = 2
  max_size             = 10
  tag {
    key                 = "name"
    value               = "Terraform-ASG-Terraform_Instance"
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
