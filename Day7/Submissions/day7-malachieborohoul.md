# Day 7: Understanding Terraform State Part 2

## Participant Details
- **Name:** BOROHOUL Soguelni Malachie
- **Task Completed:** I worked with both Workspace and Layer Isolation methods and understood their advantages and disadvantages in an enterprise context. I created a state storage and state locking environments. I also wrote a blog post to explain the difference between the 2 isolation methods in an enterprise scale.
- **Date and Time:** 8/27/2024 10:32 PM


#Restructure how web cluster with the Layer Isolation method

##globale/s3/main.tf
```hcl
provider "aws" {
  region = "us-east-2"
}



# Create an S3 bucket for Terraform state storage
resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-bsm-my-state"
  # Prevent accidental deletion of this S3 bucket
  lifecycle {
    prevent_destroy = true
  }
}

# Enable versioning so you can see the full revision history of your state files
resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable server-side encryption by default
resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.terraform_state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Explicitly block all public access to the S3 bucket
resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Create a DynamoDB table for Terraform state locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-up-and-running-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

# Terraform backend configuration using the created S3 bucket and DynamoDB table
terraform {
  backend "s3" {
    bucket         = "terraform-bsm-my-state" # Use the bucket we created
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "terraform-up-and-running-locks"
    encrypt        = true
  }
}


```

##globale/s3/outputs.tf
```hcl
output "s3_bucket_arn" {
  value       = aws_s3_bucket.terraform_state.arn
  description = "The ARN of the S3 bucket"
}
output "dynamodb_table_name" {
  value       = aws_dynamodb_table.terraform_locks.name
  description = "The name of the DynamoDB table"
}

```

#stage/services/webserver-cluster/main.tf
```hcl
# Provider Configuration
provider "aws" {
  region = "us-east-1"
}


# Data Sources
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Random Pet Resources
resource "random_pet" "sg_instance_name" {
  prefix = "terraform-example-instance"
  length = 2
}

resource "random_pet" "sg_alb_name" {
  prefix = "terraform-example-alb"
  length = 2
}

resource "random_pet" "lb_name" {
  prefix = "terraform-asg"
  length = 2
}

resource "random_pet" "tg_name" {
  prefix = "terraform-asg"
  length = 2
}

# EC2 and Auto Scaling Resources
resource "aws_launch_configuration" "example" {
  image_id        = "ami-0b0ea68c435eb488d"
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.instance.id]

 # Render the User Data script as a template
      user_data = templatefile("user-data.sh", {
        server_port = var.server_port
        db_address  = data.terraform_remote_state.db.outputs.address
        db_port     = data.terraform_remote_state.db.outputs.port
})

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "example" {
  launch_configuration = aws_launch_configuration.example.name
  vpc_zone_identifier  = data.aws_subnets.default.ids
  target_group_arns    = [aws_lb_target_group.asg.arn]
  health_check_type    = "ELB"
  min_size             = 2
  max_size             = 10

  tag {
    key                 = "Name"
    value               = "terraform-asg-example"
    propagate_at_launch = true
  }
}

# Security Group Resources
resource "aws_security_group" "instance" {
  name = random_pet.sg_instance_name.id

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "alb" {
  name = random_pet.sg_alb_name.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Load Balancer Resources
resource "aws_lb" "example" {
  name               = random_pet.lb_name.id
  load_balancer_type = "application"
  subnets            = data.aws_subnets.default.ids
  security_groups    = [aws_security_group.alb.id]
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.example.arn
  port              = 80
  protocol          = "HTTP"

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
  name     = random_pet.tg_name.id
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

data "terraform_remote_state" "db" {
      backend = "s3"
      config = {
        bucket = "terraform-bsm-my-state"
        key    = "stage/data-stores/mysql/terraform.tfstate"
        region = "us-east-2"
} 
}

```

##stage/services/webserver-cluster/outputs.tf
```hcl
# Outputs
output "alb_dns_name" {
  value       = aws_lb.example.dns_name
  description = "The domain name of the load balancer"
}
```

#stage/services/webserver-cluster/variables.tf
```hcl

# Variables
variable "server_port" {
  type        = number
  default     = 8080
  description = "The port the server will use for HTTP requests"
}
```

##stage/services/webserver-cluster/user-data.sh
```bash

#!/bin/bash
cat > index.html <<EOF
<h1>Hello, World</h1>
<p>DB address: ${db_address}</p>
<p>DB port: ${db_port}</p>
EOF
```