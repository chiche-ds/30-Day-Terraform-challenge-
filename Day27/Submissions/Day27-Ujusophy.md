# Day 27: 3-Tier Multi-Region High Availability Infrastructure with AWS and Terraform
## Participant Details

- **Name:** Njoku Ujunwa Sophia 
- **Task Completed:** 3-tier multi-region infrastructure using AWS and Terraform. This architecture will ensure high availability and fault tolerance by distributing traffic across multiple AWS regions.
- **Date and Time:** 27/09/2024 08:30 AM

### modules/alb
##### - main.tf
```hcl
resource "aws_lb" "main" {
  name               = "${var.name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.security_group_id]
  subnets            = var.public_subnets

  tags = {
    Name = "${var.name}-alb"
  }
}

resource "aws_lb_target_group" "main" {
  name     = "${var.name}-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    protocol = "HTTP"
    path     = "/"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main.arn
  }
}

resource "aws_lb" "main_us_west" {
  provider           = aws.us-west
  name               = "${var.name}-alb-us-west"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.security_group_id]
  subnets            = var.public_subnets

  tags = {
    Name = "${var.name}-alb-us-west"
  }
}

resource "aws_lb_target_group" "main_us_west" {
  provider = aws.us-west
  name     = "${var.name}-target-group-us-west"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    protocol = "HTTP"
    path     = "/"
  }
}

resource "aws_lb_listener" "http_us_west" {
  provider           = aws.us-west
  load_balancer_arn  = aws_lb.main_us_west.arn
  port               = 80
  protocol           = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main_us_west.arn
  }
}
```
##### - variables.tf
```hcl
variable "name" {
  type        = string
  description = "Name prefix for ALB resources"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID where the ALB will be deployed"
}

variable "public_subnets" {
  type        = list(string)
  description = "List of public subnet IDs"
}

variable "security_group_id" {
  type        = string
  description = "Security group ID for the ALB"
}
```
##### - outputs.tf
```hcl
output "alb_dns_name" {
  value = aws_lb.main.dns_name
}

output "main_target_group_arn" {
  description = "The ARN of the main target group"
  value       = aws_lb_target_group.main.arn 
}

output "dns_name" {
  description = "The DNS name of the ALB"
  value       = aws_lb.main.dns_name
}

output "zone_id" {
  description = "The zone ID of the ALB"
  value       = aws_lb.main.zone_id
}

output "alb_name" {
  description = "The name of the ALB"
  value       = aws_lb.main.name
}

output "elb_us_east_dns" {
  value = aws_lb.main.dns_name
}

output "elb_us_east_zone_id" {
  value = aws_lb.main.zone_id
}

output "elb_us_west_dns" {
  value = aws_lb.main_us_west.dns_name
}

output "elb_us_west_zone_id" {
  value = aws_lb.main_us_west.zone_id
}
```

### modules/asg
##### - main.tf
```hcl
resource "aws_launch_template" "app" {
  name          = "${var.name}-launch-template"
  image_id      = var.ami_id
  instance_type = var.instance_type

  key_name = var.key_name

  network_interfaces {
    associate_public_ip_address = false
    security_groups             = [var.security_group_id]
    subnet_id                   = element(var.private_subnets, 0)
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "${var.name}-app-instance"
    }
  }

  user_data = base64encode(<<-EOF
    #!/bin/bash
    echo "Hello from  ASG instance!" > /var/www/html/index.html
    systemctl start httpd
  EOF
  )
}

resource "aws_autoscaling_group" "asg" {
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  vpc_zone_identifier = var.private_subnets
  min_size            = var.min_size
  max_size            = var.max_size
  desired_capacity    = var.desired_capacity

  target_group_arns = [var.target_group_arn]

  tag {
    key                 = "Name"
    value               = "${var.name}-app-instance"
    propagate_at_launch = true
  }
}

data "aws_instances" "app_instances" {
  instance_tags = {
    Name = "${var.name}-app-instance"
  }
}

data "aws_autoscaling_group" "app" {
  name = aws_autoscaling_group.asg.name
}
```
##### - variables.tf
```hcl
variable "ami_id" {
  type        = string
  description = "AMI ID for the EC2 instances"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type"
}

variable "key_name" {
  type        = string
  description = "EC2 Key Pair Name"
}

variable "private_subnets" {
  type        = list(string)
  description = "List of private subnet IDs"
}

variable "security_group_id" {
  type        = string
  description = "Security group ID for EC2 instances"
}

variable "min_size" {
  type        = number
  description = "Minimum number of instances in ASG"
}

variable "max_size" {
  type        = number
  description = "Maximum number of instances in ASG"
}

variable "desired_capacity" {
  type        = number
  description = "Desired number of instances in ASG"
}

variable "target_group_arn" {
  type        = string
  description = "Target group ARN for the Load Balancer"
}

variable "name" {
  type        = string
  description = "Name prefix for the ASG resources"
}
```
##### - outputs.tf
```hcl
output "asg_name" {
  value = aws_autoscaling_group.asg.name
}

output "launch_template_id" {
  value = aws_launch_template.app.id
}
```

### modules/cloudwatch
##### - main.tf
```hcl
resource "aws_cloudwatch_metric_alarm" "ec2_cpu_alarm" {
  alarm_name          = "${var.name}-ec2-cpu-utilization"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 120
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "This metric monitors EC2 instance CPU utilization"
  dimensions = {
    InstanceId = var.ec2_instance_id
  }
}

resource "aws_cloudwatch_metric_alarm" "elb_latency_alarm" {
  alarm_name          = "${var.name}-elb-latency"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Latency"
  namespace           = "AWS/ELB"
  period              = 60
  statistic           = "Average"
  threshold           = 0.5
  alarm_description   = "This metric monitors ELB latency"
  dimensions = {
    LoadBalancerName = var.elb_name
  }
}

resource "aws_cloudwatch_metric_alarm" "rds_cpu_alarm" {
  alarm_name          = "${var.name}-rds-cpu-utilization"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = 120
  statistic           = "Average"
  threshold           = 75
  alarm_description   = "This metric monitors RDS CPU utilization"
  dimensions = {
    DBInstanceIdentifier = var.rds_instance_id
  }
}
```
##### - variables.tf
```hcl
variable "name" {
  type        = string
  description = "Name prefix for the CloudWatch alarms"
}

variable "ec2_instance_id" {
  type        = string
  description = "EC2 instance ID for monitoring"
}

variable "elb_name" {
  type        = string
  description = "ELB name for monitoring"
}

variable "rds_instance_id" {
  type        = string
  description = "RDS instance ID for monitoring"
}
```
##### - outputs.tf
```hcl
output "ec2_cpu_alarm_arn" {
  value = aws_cloudwatch_metric_alarm.ec2_cpu_alarm.arn
}

output "elb_latency_alarm_arn" {
  value = aws_cloudwatch_metric_alarm.elb_latency_alarm.arn
}

output "rds_cpu_alarm_arn" {
  value = aws_cloudwatch_metric_alarm.rds_cpu_alarm.arn
}
```

### modules/health_check
##### - main.tf
```hcl
resource "aws_route53_health_check" "primary" {
  fqdn             = var.elb_us_east_dns
  type             = "HTTP"
  port             = 80
  resource_path    = "/"
  failure_threshold = 3
  request_interval  = 30
}

resource "aws_route53_health_check" "secondary" {
  fqdn             = var.elb_us_west_dns
  type             = "HTTP"
  port             = 80
  resource_path    = "/"
  failure_threshold = 3
  request_interval  = 30
}
```
##### - variables.tf
```hcl
variable "elb_us_east_dns" {
  type        = string
  description = "DNS name for the ELB in us-east-1"
}

variable "elb_us_west_dns" {
  type        = string
  description = "DNS name for the ELB in us-west-2"
}

variable "domain_name" {
  type        = string
  description = "Domain name for the health check"
}

variable "elb_us_east_zone_id" {
  type        = string
  description = "Zone ID for the ELB in us-east-1"
}

variable "elb_us_west_zone_id" {
  type        = string
  description = "Zone ID for the ELB in us-west-2"
}

variable "zone_id" {
  type        = string
  description = "The ID of the Route53 hosted zone"
}
```
##### - outputs.tf
```hcl
output "primary_health_check_id" {
  value = aws_route53_health_check.primary.id
}

output "secondary_health_check_id" {
  value = aws_route53_health_check.secondary.id
}
```

### modules/rds
##### - main.tf
```hcl
resource "aws_db_instance" "primary" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  identifier                = var.db_name
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.mysql8.0"
  publicly_accessible  = false
  vpc_security_group_ids = [var.security_group_id]
  db_subnet_group_name = var.subnet_group

  multi_az            = true
  availability_zone   = var.primary_az
  backup_retention_period = 7
  skip_final_snapshot = true

  tags = {
    Name = "${var.name}-primary-rds"
  }
}

resource "aws_db_instance" "replica" {
  count = var.create_replica ? 1 : 0
  identifier              = "${var.name}-read-replica"
  engine                  = aws_db_instance.primary.engine
  engine_version          = aws_db_instance.primary.engine_version
  instance_class          = aws_db_instance.primary.instance_class
  replicate_source_db     = aws_db_instance.primary.id 
  publicly_accessible     = false
  vpc_security_group_ids  = [var.security_group_id]
  db_subnet_group_name    = var.subnet_group
  availability_zone       = var.replica_az

  tags = {
    Name = "${var.name}-read-replica"
  }
}

resource "aws_db_subnet_group" "your_db_subnet_group_name" {
  name       = "${var.name}-db-subnet-group"
  subnet_ids = var.subnet_ids
  tags = {
    Name = "${var.name}-db-subnet-group"
  }
}
```
##### - variables.tf
```hcl
variable "name" {
  type        = string
  description = "Name prefix for RDS resources"
}

variable "db_name" {
  type        = string
  description = "Database name"
}

variable "db_username" {
  type        = string
  description = "Database username"
}

variable "db_password" {
  type        = string
  description = "Database password"
  sensitive   = true
}

variable "primary_az" {
  type        = string
  description = "Availability Zone for the primary RDS instance"
}

variable "replica_az" {
  type        = string
  description = "Availability Zone for the RDS read replica"
}

variable "security_group_id" {
  type        = string
  description = "Security group ID for RDS instances"
}

variable "subnet_group" {
  type        = string
  description = "DB subnet group"
}

variable "create_replica" {
  type        = bool
  default     = true
  description = "Whether to create a read replica"
}

variable "subnet_ids" {
  description = "List of subnet IDs for the RDS DB subnet group"
  type        = list(string)
}
```
##### - outputs.tf
```hcl
output "primary_rds_endpoint" {
  value = aws_db_instance.primary.endpoint
}

output "read_replica_endpoints" {
  value = [for i in range(length(aws_db_instance.replica)) : aws_db_instance.replica[i].endpoint]
}

output "primary_rds_arn" {
  value = aws_db_instance.primary.arn
}

output "db_subnet_group" {
  value = aws_db_subnet_group.your_db_subnet_group_name
}

output "primary_rds_instance_id" {
  value = aws_db_instance.primary.id
}
```

### modules/route53
##### - main.tf
```hcl
resource "aws_route53_record" "primary" {
  zone_id = var.zone_id
  name    = var.domain_name
  type    = "A"

  alias {
    name                   = var.elb_us_east_dns
    zone_id                = var.elb_us_east_zone_id
    evaluate_target_health = true
  }

  failover_routing_policy {
    type           = "PRIMARY"
    set_identifier = "primary"
  }

  health_check_id = var.primary_health_check_id
}

resource "aws_route53_record" "secondary" {
  zone_id = var.zone_id
  name    = var.domain_name
  type    = "A"

  alias {
    name                   = var.elb_us_west_dns
    zone_id                = var.elb_us_west_zone_id
    evaluate_target_health = true
  }

  failover_routing_policy {
    type           = "SECONDARY"
    set_identifier = "secondary"
  }

  health_check_id = var.secondary_health_check_id
}
```
##### - variables.tf
```hcl
variable "elb_us_east_dns" {
  type        = string
  description = "DNS name for the ELB in us-east-1"
}

variable "elb_us_west_dns" {
  type        = string
  description = "DNS name for the ELB in us-west-2"
}

variable "domain_name" {
  type        = string
  description = "Domain name for the health check"
}

variable "elb_us_east_zone_id" {
  type        = string
  description = "Zone ID for the ELB in us-east-1"
}

variable "elb_us_west_zone_id" {
  type        = string
  description = "Zone ID for the ELB in us-west-2"
}

variable "zone_id" {
  type        = string
  description = "The ID of the Route53 hosted zone"
}

variable "primary_health_check_id" {
  description = "The health check ID for the primary Route53 record"
  type        = string
}

variable "secondary_health_check_id" {
  description = "The health check ID for the secondary Route53 record"
  type        = string
}
```
##### - outputs.tf
```hcl
output "primary_dns" {
  value = aws_route53_record.primary.fqdn
}

output "secondary_dns" {
  value = aws_route53_record.secondary.fqdn
}
```

### modules/s3
##### - main.tf
```hcl
resource "aws_s3_bucket" "source" {
  bucket = "${var.name}-source"
  acl    = "private"

  versioning {
    enabled = true
  }

  tags = {
    Name = "${var.name}-source"
  }
}

resource "aws_s3_bucket" "destination" {
  bucket = "${var.name}-destination"
  acl    = "private"

  versioning {
    enabled = true
  }

  tags = {
    Name = "${var.name}-destination"
  }
}

# Create IAM role for replication
resource "aws_iam_role" "s3_replication_role" {
  name = "s3-replication-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "s3.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

# Attach policy to the role
resource "aws_iam_role_policy" "s3_replication_policy" {
  role = aws_iam_role.s3_replication_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObjectVersion",
        "s3:GetObjectVersionAcl"
      ]
      Resource = "${aws_s3_bucket.source.arn}/*"
    },
    {
      Effect = "Allow"
      Action = [
        "s3:ReplicateObject",
        "s3:ReplicateDelete"
      ]
      Resource = "${aws_s3_bucket.destination.arn}/*"
    }]
  })
}

# Configure replication rule
resource "aws_s3_bucket_replication_configuration" "replication" {
  role = aws_iam_role.s3_replication_role.arn
  bucket = aws_s3_bucket.source.bucket

  rule {
    id = "replication-rule"
    status = "Enabled"

    filter {
      prefix = ""  # Replicate all objects
    }

    destination {
      bucket = aws_s3_bucket.destination.arn
      storage_class = "STANDARD"
    }
  }
}
```
##### - variables.tf
```hcl
variable "name" {
  type        = string
  description = "Name prefix for the S3 buckets"
}
```
##### - outputs.tf
```hcl
output "source_bucket_arn" {
  value = aws_s3_bucket.source.arn
}

output "destination_bucket_arn" {
  value = aws_s3_bucket.destination.arn
}
```

### modules/vpc
##### - main.tf
```hcl
resource "aws_vpc" "main" {
  cidr_block = var.cidr_block
  tags = {
    Name = "${var.name}-vpc"
  }
}

resource "aws_subnet" "public" {
  count = length(var.public_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnets[count.index]
  availability_zone = var.public_azs[count.index]
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.name}-public-subnet-${count.index}"
  }
}

resource "aws_subnet" "private" {
  count = length(var.private_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnets[count.index]
  availability_zone = var.private_azs[count.index]
  tags = {
    Name = "${var.name}-private-subnet-${count.index}"
  }
}

resource "aws_db_subnet_group" "example" {
  name       = "${var.name}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id
  tags = {
    Name = "${var.name}-db-subnet-group"
  }
}
```
##### - variables.tf
```hcl
variable "cidr_block" {
  type        = string
  description = "CIDR block for the VPC"
}

variable "public_subnets" {
  type        = list(string)
  description = "List of public subnet CIDR blocks"
}

variable "private_subnets" {
  type        = list(string)
  description = "List of private subnet CIDR blocks"
}

variable "public_azs" {
  type        = list(string)
  description = "List of availability zones for public subnets"
}

variable "private_azs" {
  type        = list(string)
  description = "List of availability zones for private subnets"
}

variable "name" {
  type        = string
  description = "Name prefix for resources"
}
```
##### - outputs.tf
```hcl
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}

output "db_subnet_group" {
  value = aws_db_subnet_group.example.name
}

output "private_subnets" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}
```

### main.tf
```hcl
provider "aws" {
  region = "us-west-2"
  alias  = "us-west"
}

provider "aws" {
  region = "us-east-1"
  alias  = "us-east"
}

module "vpc_us_east" {
  source          = "./modules/vpc"
  cidr_block      = "10.0.0.0/16"
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets = ["10.0.3.0/24", "10.0.4.0/24"]
  public_azs      = ["us-east-1a", "us-east-1b"]
  private_azs     = ["us-east-1a", "us-east-1b"]
  name            = "us-east"
}

module "vpc_us_west" {
  source          = "./modules/vpc"
  providers       = { aws = aws.us-west }  # Corrected alias here
  cidr_block      = "10.1.0.0/16"
  public_subnets  = ["10.1.1.0/24", "10.1.2.0/24"]
  private_subnets = ["10.1.3.0/24", "10.1.4.0/24"]
  public_azs      = ["us-west-2a", "us-west-2b"]
  private_azs     = ["us-west-2a", "us-west-2b"]
  name            = "us-west"
}

resource "aws_security_group" "alb_sg" {
  vpc_id = module.vpc_us_east.vpc_id

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

  tags = {
    Name = "alb-sg"
  }
}

module "alb_us_east" {
  source            = "./modules/alb"
  providers         = { aws = aws.us-east }  
  name              = "us-east"
  vpc_id            = module.vpc_us_east.vpc_id
  public_subnets    = module.vpc_us_east.public_subnet_ids
  security_group_id = aws_security_group.alb_sg.id
}

module "alb_us_west" {
  source            = "./modules/alb"
  providers         = { aws = aws.us-west } 
  name              = "us-west"
  vpc_id            = module.vpc_us_west.vpc_id
  public_subnets    = module.vpc_us_west.public_subnet_ids
  security_group_id = aws_security_group.alb_sg.id
}

resource "aws_lb_target_group" "main" {
  name     = "main-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = module.vpc_us_west.vpc_id
}

resource "aws_security_group" "app_sg" {
  vpc_id = module.vpc_us_east.vpc_id

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

  tags = {
    Name = "app-sg"
  }
}

module "asg_us_east" {
  source            = "./modules/asg"
  name              = "us-east"
  ami_id            = "ami-0a0e5d9c7acc336f1" 
  instance_type     = "t2.micro"
  key_name          = "techynurse"
  private_subnets   = module.vpc_us_east.private_subnet_ids
  security_group_id = aws_security_group.app_sg.id
  min_size          = 2
  max_size          = 4
  desired_capacity  = 2
  target_group_arn  = module.alb_us_east.main_target_group_arn
}

module "asg_us_west" {
  source            = "./modules/asg"
  providers         = { aws = aws.us-west }
  name              = "us-west"
  ami_id            = "ami-0c55b159cbfafe1f0" 
  instance_type     = "t2.micro"
  key_name          = "your-key-name"
  private_subnets   = module.vpc_us_west.private_subnet_ids
  security_group_id = aws_security_group.app_sg.id
  min_size          = 2
  max_size          = 4
  desired_capacity  = 2
  target_group_arn  = module.alb_us_west.main_target_group_arn
}

resource "aws_security_group" "rds_sg" {
  vpc_id = module.vpc_us_east.vpc_id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds-sg"
  }
}

module "rds_us_east" {
  source            = "./modules/rds"
  name              = "us-east"
  db_name           = "appdb"
  db_username       = "admin"
  db_password       = "yourpassword"
  primary_az        = "us-east-1a"
  replica_az        = "us-east-1b" 
  security_group_id = aws_security_group.rds_sg.id
  subnet_group      = module.vpc_us_east.db_subnet_group
  subnet_ids        = module.vpc_us_east.private_subnets
}

module "rds_us_west" {
  source            = "./modules/rds"
  providers         = { aws = aws.us-west }
  name              = "us-west"
  db_name           = "appdb"
  db_username       = "admin"
  db_password       = "yourpassword"
  primary_az        = "us-west-2a"
  replica_az        = "us-west-2b"
  security_group_id = aws_security_group.rds_sg.id
  subnet_group      = module.vpc_us_west.db_subnet_group
  create_replica    = true
  subnet_ids        = module.vpc_us_west.private_subnets
}

module "route53_dns" {
  source                      = "./modules/route53"
  zone_id                     = var.zone_id
  domain_name                 = var.domain_name
  elb_us_east_dns             = aws_lb.main.dns_name 
  elb_us_east_zone_id         = aws_lb.main.zone_id        
  elb_us_west_dns             = aws_lb.main_us_west.dns_name
  elb_us_west_zone_id         = aws_lb.main_us_west.zone_id  
  primary_health_check_id     = module.health_check_module.primary_health_check_id
  secondary_health_check_id   = module.health_check_module.secondary_health_check_id
}

module "health_check_module" {
  source                      = "./modules/health_check"
  elb_us_east_dns             = aws_lb.main.dns_name
  elb_us_west_dns             = aws_lb.main_us_west.dns_name
  domain_name                 = var.domain_name
  elb_us_east_zone_id         = aws_lb.main.zone_id
  elb_us_west_zone_id         = aws_lb.main_us_west.zone_id
  zone_id                     = var.zone_id
}

# S3 Replication in us-east-1 to us-west-2
module "s3_replication" {
  source = "./modules/s3"
  name   = "app-static-assets"
}

module "cloudwatch_alarms" {
  source             = "./modules/cloudwatch"
  name               = "app-monitoring"
  ec2_instance_id    = data.aws_instances.app_instances.ids[0]
  elb_name           = module.alb_us_east.dns_name  
  rds_instance_id    = module.rds_us_east.primary_rds_instance_id  
}

data "aws_instances" "app_instances" {
  instance_tags = {
    Name = "first-app-instance"
  }
}
```
### variables.tf
```hcl
variable "zone_id" {
  description = "The ID of the Route53 hosted zone"
  default        = "Z0920715NC80YK7KBOAC"
}

variable "domain_name" {
  description = "The domain name for Route 53 records"
  default     = "techynurse.site"
}
```
