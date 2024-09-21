```hcl
provider "aws" {
region = "us-east-1"
}

data "aws_vpc" "default" {
default = true
}

data "aws_subnets" "default" {
filter {
name = "vpc-id"
values = [data.aws_vpc.default.id]
}
}


resource "aws_launch_configuration" "example" {
image_id = "ami-04a81a99f5ec58529"
instance_type = "t2.micro"
security_groups = [aws_security_group.instance.id]
user_data = <<-EOF
#!/bin/bash
echo "Hello, World" > index.html
nohup busybox httpd -f -p ${var.server_port} &
EOF

# Required when using a launch configuration with an auto scaling group.
lifecycle {
create_before_destroy = true
}
}

resource "aws_autoscaling_group" "example" {
launch_configuration = aws_launch_configuration.example.name
vpc_zone_identifier = data.aws_subnets.default.ids
min_size = 2
max_size = 10
tag {
key = "Name"
value = "terraform-asg-example"
propagate_at_launch = true
}
}

resource "aws_security_group" "instance" {
name = "terraform-example-instance"
ingress {
from_port = var.server_port
to_port = var.server_port
protocol = "tcp"
cidr_blocks = ["0.0.0.0/0"]
}
}

locals {
  service_name = "Automation"
  app_team     = "Cloud Team"
  createdby    = "terraform"
}

resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"


 tags = {
    "Service"   = local.service_name
    "AppTeam"   = local.app_team
    "CreatedBy" = local.createdby
  }

}
locals {
  # Common tags to be assigned to all resources
  common_tags = {
    Name      = var.server_name
    Owner     = "cloud-team"
    App       = "Ada-app"
    Service   = local.service_name
    AppTeam   = local.app_team
    CreatedBy = local.createdby
 } 
}

variable "server_name" {
  type        = string
  description = "Name of the server"
}

resource "aws_instance" "web_server" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.public_subnets["public_subnet_1"].id
  
  tags = local.common_tags
}
```
