# Day 5: Scaling Infrastructure

## Participant Details
- **Name:** Musyoka Kilonzo
- **Task Completed:** Scaling clustered web servers using Terraform to handle increased load.Completed Chapter 2 and started Chapter 3 how to manage state.
- **Date and Time:** 8/24/2024 23:10PM

## Terraform Code - Scaling the infrastructure using autoscaling group and ALB.
### main.tf

```hcl
# Now you can create the ASG itself using the aws_autoscaling_group resource:
resource "aws_autoscaling_group" "clustered-servers" {
  launch_configuration = aws_launch_configuration.clustered-servers.name
  vpc_zone_identifier = tolist([for subnet in aws_subnet.public_subnets : subnet.id])
  target_group_arns = [aws_lb_target_group.asg.arn]
  health_check_type = "ELB"
  min_size = 2
  max_size = 5
  tag {
    key = "name"
    value = "musyoka-clustered-servers-asg"
    propagate_at_launch = true
  } 
}

# Deploy Application Load Balancer(ALB)
## The first step is to create the ALB itself using the aws_lb resource:
resource "aws_lb" "alb" {
 name = "musyoka-alb"
 load_balancer_type = "application"
 subnets = tolist([for subnet in aws_subnet.public_subnets : subnet.id])
 security_groups = [aws_security_group.alb.id]
}
## The next step is to define a listener for this ALB using the aws_lb_listener resource:
resource "aws_lb_listener" "http" {
 load_balancer_arn = aws_lb.alb.arn
 port = 80
 protocol = "HTTP"

# By default, return a simple 404 page
 default_action {
 type = "fixed-response"
 fixed_response {
 content_type = "text/plain"
 message_body = "404: page not found"
 status_code = 404
 }
 }
}
# ALB security Group
resource "aws_security_group" "alb" {
 name = "musyoka-alb-security-group"
 vpc_id = aws_vpc.vpc.id
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

# create a target group for your ASG using the aws_lb_target_group resource:

resource "aws_lb_target_group" "asg" {
 name = "musyoka-asg-target-group"
 port = var.server_port
 protocol = "HTTP"
 vpc_id = aws_vpc.vpc.id
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
#tie all these pieces together by creating listener rules using the aws_lb_listener_rule resource:

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

# Create s3 bucket for storing our state file
resource "aws_s3_bucket" "terraform_state" {
 bucket = "musyokaterraforms3"
 # Prevent accidental deletion of this S3 bucket
 lifecycle {
 prevent_destroy = true
 }
}
# Enable versioning so you can see the full revision history of your
# state files
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
 bucket = aws_s3_bucket.terraform_state.id
 block_public_acls = true
 block_public_policy = true
 ignore_public_acls = true
 restrict_public_buckets = true
}
resource "aws_dynamodb_table" "terraform_locks" {
 name = "terraform-up-and-running-locks"
 billing_mode = "PAY_PER_REQUEST"
 hash_key = "LockID"
  attribute {
 name = "LockID"
 type = "S"
 }
}
```
### backend.tf

```hcl
terraform {
 backend "s3" {
 # Replace this with your bucket name!
 bucket = "musyokaterraforms3"
 key = "global/s3/terraform.tfstate"
 region = "us-east-1"
 # Replace this with your DynamoDB table name!
 dynamodb_table = "terraform-up-and-running-locks"
 encrypt = true
 }
}
```





