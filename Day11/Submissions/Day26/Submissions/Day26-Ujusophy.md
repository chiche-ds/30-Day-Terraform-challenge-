# Day 25: Build a Scalable Web Application with Auto Scaling on AWS
## Participant Details

- **Name:** Njoku Ujunwa Sophia 
- **Task Completed:** deploying a scalable web application using AWS EC2 instances, an Elastic Load Balancer (ELB), and Auto Scaling to dynamically adjust the number of EC2 instances based on traffic.
- **Date and Time:** 27/09/2024 08:01 AM

## GitHub repo link
https://github.com/Ujusophy/Day26-terraform-challenge


### modules/ec2/main.tf
```hcl
resource "aws_instance" "web" {
  count         = var.instance_count
  ami           = var.ami
  instance_type = var.instance_type

  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name = "WebInstance-${count.index + 1}"
  }
}

resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Allow HTTP and HTTPS traffic"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
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
```
### modules/ec2/outputs.tf
```hcl
output "web_sg_id" {
  description = "The ID of the web security group"
  value       = aws_security_group.web_sg.id  
}
```
### modules/ec2/variables.tf
```hcl
variable "instance_count" {
  description = "Number of EC2 instances"
  default       = 2
}

variable "ami" {
  description = "AMI ID for the EC2 instances"
  default      = "ami-0a0e5d9c7acc336f1"
}

variable "instance_type" {
  description = "EC2 instance type"
  default       = "t2-micro"
}
```

### modules/asg/main.tf
```hcl
resource "aws_autoscaling_group" "web" {
  desired_capacity     = var.desired_capacity
  max_size             = var.max_size
  min_size             = var.min_size
  vpc_zone_identifier  = var.subnet_ids

  launch_configuration = aws_launch_configuration.web.id

  tag {
    key                 = "Name"
    value               = "WebInstance"
    propagate_at_launch = true
  }
}

resource "aws_launch_configuration" "web" {
  name          = "web-launch-config"
  image_id      = var.ami
  instance_type = var.instance_type
  security_groups = [var.security_group_id]  
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "cpu-high-${var.asg_name}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name        = "CPUUtilization"
  namespace          = "AWS/EC2"
  period             = "60"
  statistic          = "Average"
  threshold          = 75  
  alarm_description  = "This metric monitors CPU utilization and triggers scaling actions."

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.web.name
  }

  alarm_actions = [aws_autoscaling_policy.scale_up.arn]
  ok_actions    = [aws_autoscaling_policy.scale_down.arn]
}

resource "aws_cloudwatch_metric_alarm" "cpu_low" {
  alarm_name          = "cpu-low-${var.asg_name}"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "2"
  metric_name        = "CPUUtilization"
  namespace          = "AWS/EC2"
  period             = "60"
  statistic          = "Average"
  threshold          = 20  
  alarm_description  = "This metric monitors CPU utilization and triggers scaling actions."

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.web.name
  }

  alarm_actions = [aws_autoscaling_policy.scale_down.arn]
}

resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up-${var.asg_name}"
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment      = 1
  cooldown               = 300  
  autoscaling_group_name = aws_autoscaling_group.web.name
}

resource "aws_autoscaling_policy" "scale_down" {
  name                   = "scale-down-${var.asg_name}"
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment      = -1
  cooldown               = 300 
  autoscaling_group_name = aws_autoscaling_group.web.name
}
```
### modules/asg/variables.tf
```hcl
variable "desired_capacity" {
  description = "Desired number of instances in the ASG"
  type        = number
}

variable "max_size" {
  description = "Maximum number of instances in the ASG"
  type        = number
}

variable "min_size" {
  description = "Minimum number of instances in the ASG"
  type        = number
}

variable "subnet_ids" {
  description = "List of subnet IDs for the ASG"
  type        = list(string)
}

variable "ami" {
  description = "AMI ID for the launch configuration"
  default      = "ami-0a0e5d9c7acc336f1"
}

variable "instance_type" {
  description = "Instance type for the launch configuration"
  default      = "t2-micro"
}

variable "security_group_id" {
  description = "The security group ID to associate with the launch configuration"
  type        = string
}

variable "asg_name" {
  description = "Name of the Auto Scaling Group"
  default       = "asg1"
}
```

### modules/elb/main.tf
```hcl
resource "aws_elb" "web" {
  name               = var.elb_name
  availability_zones = var.availability_zones

  listener {
    instance_port     = 80
    instance_protocol = "HTTP"
    lb_port           = 80
    lb_protocol       = "HTTP"
  }

  health_check {
    target              = "HTTP:80/"
    interval            = 30
    timeout             = 5
    healthy_threshold  = 2
    unhealthy_threshold = 2
  }

  tags = {
    Name = var.elb_name
  }
}
```
### modules/elb/variables.tf
```hcl
variable "elb_name" {
  description = "Name of the ELB"
  default        = "elb1"
}

variable "availability_zones" {
  description = "The availability zones for the ELB"
  default     = ["us-east-1a", "us-east-1b"]
}
```

### main.tf
```hcl
module "ec2" {
  source = "./modules/ec2"
  ami           = "ami-0a0e5d9c7acc336f1"  
  instance_type = "t2.micro"
  instance_count = 2
}

module "elb" {
  source = "./modules/elb"
  elb_name           = "my-elb"
  availability_zones = ["us-east-1a", "us-east-1b"]  
}

module "asg" {
  source = "./modules/asg"
  desired_capacity = 2
  max_size         = 5
  min_size         = 1
  subnet_ids       = ["subnet-0b80d1672c1d6452a", "subnet-0846e4641e585a3df"] 
  ami              = "ami-0a0e5d9c7acc336f1"  
  instance_type    = "t2.micro"
  security_group_id = module.ec2.web_sg_id 
  asg_name          = "asg1"
}
```
### backend.tf
```hcl
# S3 Bucket for Terraform State
resource "aws_s3_bucket" "terraform_state" {
  bucket = "techynurse-terraform-state-bucket"  # Replace with a unique bucket name
  acl    = "private"

  versioning {
    enabled = true
  }

  lifecycle {
    prevent_destroy = true  # Prevent accidental deletion of the bucket
  }

  tags = {
    Name        = "TerraformStateBucket"
    Environment = "dev"
  }
}


resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  attribute {
    name = "LockID"
    type = "S"
  }
  hash_key = "LockID"

  tags = {
    Name        = "TerraformLocksTable"
    Environment = "dev"
  }
}

terraform {
  backend "s3" {
    bucket         = "techynurse-terraform-state-bucket"  
    key            = "terraform/state"
    region         = "us-east-1"  # Update to match your desired region
    dynamodb_table = "terraform-locks"  # Use the table name directly
    encrypt        = true
  }
}
```
