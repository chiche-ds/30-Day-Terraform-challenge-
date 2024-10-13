
# Day5: Scaling Infrastructure

### Name: Ajibola Mubarak
### Task Completed: Day 4: I deployed a load balancer to distribute traffic across your servers and to give all my users the IP (actually, the DNS name) of the load balancer. I also made social media posts
### Date: 10/10/24
### Time: 3:09am


### This is the `main.tf` with all the configurations  
```hcl

| Block Type  | Use Case                             | Code Sample                                   |
|-----------------|-----------------------------------------|---------------------------------------------------|
| Provider     | Configures the cloud provider (e.g., AWS, Azure). | ⁠ hcl provider "aws" { region = "us-west-2" }  ⁠ |
| Resource     | Defines a single piece of infrastructure (e.g., an EC2 instance). | ⁠ hcl resource "aws_instance" "example" { ami = "ami-123456" instance_type = "t2.micro" }  ⁠ |
| Data         | Fetches information from the provider that can be used in other resources. | ⁠ hcl data "aws_ami" "latest" { most_recent = true owners = ["amazon"] }  ⁠ |

provider "aws" {
  region = "us-east-1"
}

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

#  clustered webserver with the help of Autosacling group using Terraform.
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


 # Create a listener
resource "aws_lb_listener" "http" {
 load_balancer_arn = aws_lb.example.arn
 port = 80
 protocol = "HTTP"
}

resource "aws_security_group" "alb" {
 name = "terraform-example-alb"
 # Allow inbound HTTP requests
 ingress {
 from_port = 80
 to_port = 80
 protocol = "tcp"
 cidr_blocks = ["0.0.0.0/0"]
 }

 # Allow all outbound requests
 egress {
 from_port = 0
 to_port = 0
 protocol = "-1"
 cidr_blocks = ["0.0.0.0/0"]
 }
}

# Create a Application Load Balancer
resource "aws_lb" "example" {
 name = "terraform-asg-example"
 load_balancer_type = "application"
 subnets = data.aws_subnets.default.ids
 security_groups = [aws_security_group.alb.id]
}

# Create a Target Group
resource "aws_lb_target_group" "asg" {
 name = "terraform-asg-example"
 port = var.server_port
 protocol = "HTTP"
 vpc_id = data.aws_vpc.default.id
 health_check {
 path = "/"
 protocol = "HTTP"
 matcher = "200"
 interval = 15
 timeout = 3
 healthy_threshold = 2
 unhealthy_threshold = 2
 }
}

resource "aws_autoscaling_group" "example" {
 launch_configuration = aws_launch_configuration.example.name
 vpc_zone_identifier = data.aws_subnets.default.ids
 target_group_arns = [aws_lb_target_group.asg.arn]
 health_check_type = "ELB"
 min_size = 2
 max_size = 10
 tag {
 key = "Name"
 value = "terraform-asg-example"
 propagate_at_launch = true
 }
}

resource "aws_lb_listener_rule" "asg" {
 listener_arn = aws_lb_listener.http.arn
 priority = 100
 condition {
 path_pattern {
 values = ["*"]
 }
 
 }
 action {
 type = "forward"
 target_group_arn = aws_lb_target_group.asg.arn
 }
}


### This displays your `Dns load Balancer` on your terminal
output "alb_dns_name" {
 value = aws_lb.example.dns_name
 description = "The domain name of the load balancer"
}
