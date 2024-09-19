# Day 7: Understanding Terraform State

## Participant Details
- **Name:** Franklin Afolabi
- **Task Completed:** : Isolation via Workspaces and via File Layouts
- **Date and Time:** September 2 2200hrs


### Isolation Terraform Code
```
main.tf
# This is the provider block showing the region to be used

provider "aws" {
    region = "us-east-2"
}


terraform {
  backend "s3" {
    bucket = "tf-frankfolabi"
    key = "stage/services/webserver-cluster/terraform.tfstate"
    region = "us-east-2"

    dynamodb_table = "tf-locks"
    encrypt = true
  }
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

data "terraform_remote_state" "db" {
  backend = "s3"

  config = {
    bucket = "tf-frankfolabi"
    key = "stage/data-stores/mysql/terraform.tfstate"
    region = "us-east-2"
  }
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

# Create the resource block for the webserver launch configuration 
# Create a user data script the fires up when the server is launched
resource "aws_launch_configuration" "webserver" {
    image_id = "ami-0fb653ca2d3203ac1"
    instance_type = "t2.micro"
    security_groups = [aws_security_group.instance.id]

    # Render the user data script as a template 
    user_data = templatefile("user-data.sh", {
      server_port = var.server_port
      db_address = data.terraform_remote_state.db.outputs.address
      db_port = data.terraform_remote_state.db.outputs.port

    })

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

# Create the ALB
resource "aws_lb" "webserver" {
  name = "tf-example"
  load_balancer_type = "application"
  subnets = data.aws_subnets.default.ids
  security_groups = [aws_security_group.alb.id]
}

# Create the AWS listener
resource "aws_lb_listener" "webserver" {
  load_balancer_arn = aws_lb.webserver.arn
  port = 80
  protocol ="HTTP"

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body ="404: page not found"
      status_code = 404
    }
  }
}

# Create security group for load balancer
resource "aws_security_group" "alb" {
  name = "tf-example"

  # Allow inbound HTTP request
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outbound requests
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]   
  }
}

# Create target group for auto scaling group
resource "aws_lb_target_group" "webserver" {
  name = "tf-example"
  port =  var.server_port
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

# Create the ALB listerner rules
resource "aws_lb_listener_rule" "asg" {
  listener_arn = aws_lb_listener.webserver.arn
  priority = 100

  condition {
    path_pattern {
      values = ["*"]
    }
  }
  action {
    type = "forward"
    target_group_arn = aws_lb_target_group.webserver.arn
  }
}


main.tf for data-stores
provider "aws" {
  region = "us-east-2"
}

resource "aws_db_instance" "example" {
    identifier_prefix ="terraform-up-and-running"
    engine = "mysql"
    allocated_storage = 10
    instance_class = "db.t3.micro"
    skip_final_snapshot = true
    db_name = "example_database"

    username = var.db_username
    password = var.db_password
}

terraform {
  backend "s3" {
    bucket = "tf-frankfolabi"
    key = "stage/data-stores/mysql/terraform.tfstate"
    region = "us-east-2"

    dynamodb_table = "tf-locks"
    encrypt = true
  }
}

data "terraform_remote_state" "db" {
  backend = "s3"

  config = {
    bucket = "tf-frankfolabi"
    key = "stage/data-stores/mysql/terraform.tfstate"
    region = "us-east-2"
  }
}

user-data.sh
#!/bin/bash

cat > index.html << EOF
<h1>Hello, World</h1>
<p>DB address: ${db_address}</p>
<p>DB port: ${db_port}</p>
EOF

nohup busybox httpd -f -p ${server_port} &


variable.tf for data-store
variable "db_username" {
  description = "The username for the database"
  type = string
  sensitive = true
}

variable "db_password" {
  description = "The password for the database"
  type = string
  sensitive = true
}

output.tf for data-store
output "address" {
    value = aws_db_instance.example.address
    description = "Connect to the database at this endpoint"
}

output "port" {
  value = aws_db_instance.example.port
  description = "The port the database is listening on"
}