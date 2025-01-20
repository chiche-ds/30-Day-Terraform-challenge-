Day 27: 3-Tier Multi-Region High Availability Infrastructure with AWS and Terraform Questions
Name: Udeh Samuel Chibuike
Task Completed: Building a 3-Tier Multi-Region High Availability Architecture with Terraform
Date and Time: 20/1/2025 10:54pm

# Launch Template
resource "aws_launch_template" "web_template" {
  name_prefix   = "web-launch-template"
  instance_type = var.instance_type
  image_id      = var.ami_id
  user_data     = base64encode(<<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y httpd
              sudo systemctl start httpd
              sudo systemctl enable httpd
              echo "Hello from Server $(hostname)" > /var/www/html/index.html
              EOF
  )

             tags = {
    Name = "WebServer"
  }
  ##user_data     = base64encode(file(var.user_data))

  network_interfaces {
    subnet_id   = var.subnet_id
    associate_public_ip_address = true
  }
}

resource "aws_autoscaling_group" "asg" {
  desired_capacity     = var.desired_capacity
  max_size             = var.max_size
  min_size             = var.min_size
  vpc_zone_identifier  = var.subnet_ids
  launch_template {
    id      = aws_launch_template.web_template.id
    version = "$Latest"
  }

  target_group_arns = [var.target_group_arn]
}

output "asg_name" {
  value = aws_autoscaling_group.asg.name
}

variable "ami_id" {}
variable "instance_type" {}
variable "subnet_id" {}
variable "subnet_ids" {}
variable "desired_capacity" {}
variable "max_size" {}
variable "min_size" {}
#variable "user_data" {}
variable "target_group_arn" {}

# EC2
resource "aws_instance" "web-server" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id
  security_groups = [var.security_group_id]
  user_data     =  base64encode(<<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y httpd
              sudo systemctl start httpd
              sudo systemctl enable httpd
              echo "Hello from Server $(hostname)" > /var/www/html/index.html
              EOF
  )

  tags = {
    Name = "web-server-instance"
  }
}

output "instance_id" {
  value = aws_instance.web-server.id
}

variable "ami_id" {}

variable "instance_type" {}
variable "subnet_id" {}
variable "user_data" {}
variable "security_group_id" {}

# ELB

#Application Load Balancer
resource "aws_lb" "elb" {
  name               = "web-load-balancer"
  internal           = false
  load_balancer_type = "application"
  subnets            = var.subnet_ids

  security_groups = [var.elb_security_group.id]

  enable_deletion_protection = false
}

#Listener for LoadBalancer
resource "aws_lb_listener" "web_listener" {
  load_balancer_arn = aws_lb.elb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.web_target.arn
  }
}
#Target Group
resource "aws_lb_target_group" "web_target" {
  name     = "web-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
  target_type = "instance"

  health_check {
    path                = "/"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
    matcher             = "200"
  } 
}

output "elb_dns_name" {
  value = aws_lb.elb.dns_name
}

output "target_group_arn" {
  value = aws_lb_target_group.web_target.arn
  description = "ARN of the target group associated with the ELB"
}

variable "vpc_id" {}
variable "elb_security_group" {}
variable "subnet_ids" {
  description = "List of subnet IDs where the ALB will be deployed"
  type        = list(string)
}

# RDS

# Primary RDS Instance
resource "aws_db_instance" "primary" {
  allocated_storage       = var.db_allocated_storage
  engine                  = var.db_engine
  engine_version          = var.db_engine_version
  instance_class          = var.db_instance_class
  db_name                 = var.db_name
  username                = var.db_username
  password                = var.db_password
  publicly_accessible     = false
  multi_az                = true
  storage_type            = "gp2"
  vpc_security_group_ids  = [var.db_security_group_id]
  db_subnet_group_name    = aws_db_subnet_group.main.name
  backup_retention_period = var.db_backup_retention
  skip_final_snapshot     = var.skip_final_snapshot
  tags = {
    Name = "${var.db_name}-primary"
  }
}

# DB Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "${var.db_name}-subnet-group"
  subnet_ids = var.db_subnet_ids
  tags = {
    Name = "${var.db_name}-subnet-group"
  }
}

output "primary_db_endpoint" {
  description = "The endpoint of the primary RDS instance."
  value       = aws_db_instance.primary.endpoint
}

output "primary_db_arn" {
  description = "The ARN of the primary RDS instance."
  value       = aws_db_instance.primary.arn
}

# RDS Variables
variable "db_allocated_storage" {
  description = "The allocated storage in GBs for the RDS instance."
  type        = number
  default     = 20
}

variable "db_engine" {
  description = "The database engine to use (e.g., mysql, postgres)."
  type        = string
}

variable "db_engine_version" {
  description = "The version of the database engine."
  type        = string
}

variable "db_instance_class" {
  description = "The instance type of the RDS instance."
  type        = string
}

variable "db_name" {
  description = "The name of the database."
  type        = string
}

variable "db_username" {
  description = "The master username for the database."
  type        = string
}

variable "db_password" {
  description = "The master password for the database."
  type        = string
  sensitive   = true
}

variable "db_security_group_id" {
  description = "The security group ID for the RDS instance."
  type        = string
}

variable "db_subnet_ids" {
  description = "A list of subnet IDs for the RDS subnet group."
  type        = list(string)
}
variable "db_subnet_group" {
  description = " RDS subnet group."
  type        = list(string)
}
variable "db_backup_retention" {
  description = "The number of days to retain database backups."
  type        = number
  default     = 7
}

variable "skip_final_snapshot" {
  description = "Determines whether to skip the final snapshot before deleting the instance."
  type        = bool
  default     = true
}

# VPC 

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = var.vpc_name
  }
}

# Subnet_1
resource "aws_subnet" "web_subnet_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.web_subnet_1_cidr
  availability_zone       = var.subnet_1_az
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.vpc_name}-web_subnet_1"
  }
}

# Subnet_2
resource "aws_subnet" "web_subnet_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.web_subnet_2_cidr
  availability_zone       = var.subnet_2_az
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.vpc_name}-web_subnet_2"
  }
}
# Private Subnet 1
resource "aws_subnet" "app_subnet_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.app_subnet_1_cidr
  availability_zone       = var.subnet_1_az
  map_public_ip_on_launch = false  # Ensures no public IP is assigned
  tags = {
    Name = "${var.vpc_name}-app_subnet_1"
  }
}

# Private Subnet 2
resource "aws_subnet" "app_subnet_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.app_subnet_2_cidr
  availability_zone       = var.subnet_2_az
  map_public_ip_on_launch = false  # Ensures no public IP is assigned
  tags = {
    Name = "${var.vpc_name}-app_subnet_2"
  }
}
# Private db Subnet 1
resource "aws_subnet" "db_subnet_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.db_subnet_1_cidr
  availability_zone       = var.subnet_1_az
  map_public_ip_on_launch = false  # Ensures no public IP is assigned
  tags = {
    Name = "${var.vpc_name}-db_subnet_1"
  }
}

# Private db Subnet 2
resource "aws_subnet" "db_subnet_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.db_subnet_2_cidr
  availability_zone       = var.subnet_2_az
  map_public_ip_on_launch = false  # Ensures no public IP is assigned
  tags = {
    Name = "${var.vpc_name}-db_subnet_2"
  }
}
# Private Route Table
resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${var.vpc_name}-private-rt"
  }
}

# NAT Gateway for Outbound Traffic
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id  # Elastic IP for NAT Gateway
  subnet_id     = aws_subnet.web_subnet_1.id  # A public subnet
  tags = {
    Name = "${var.vpc_name}-nat-gateway"
  }
}

# Elastic IP for NAT Gateway
resource "aws_eip" "nat" {
  tags = {
    Name = "${var.vpc_name}-nat-eip"
  }
}

# Private Route Table Routes
resource "aws_route" "private_route" {
  route_table_id         = aws_route_table.private_rt.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat.id
}

# Associate Private Subnet 1 with Private Route Table
resource "aws_route_table_association" "app_subnet_1_association" {
  subnet_id      = aws_subnet.app_subnet_1.id
  route_table_id = aws_route_table.private_rt.id
}

# Associate Private Subnet 2 with Private Route Table
resource "aws_route_table_association" "app_subnet_2_association" {
  subnet_id      = aws_subnet.app_subnet_2.id
  route_table_id = aws_route_table.private_rt.id
}
# Associate db Subnet 1 with Private Route Table
resource "aws_route_table_association" "db_subnet_1_association" {
  subnet_id      = aws_subnet.db_subnet_1.id
  route_table_id = aws_route_table.private_rt.id
}

# Associate db Subnet 2 with Private Route Table
resource "aws_route_table_association" "db_subnet_2_association" {
  subnet_id      = aws_subnet.db_subnet_2.id
  route_table_id = aws_route_table.private_rt.id
}

# Database Subnet Group
resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "${var.vpc_name}-db-subnet-group"
  subnet_ids = [aws_subnet.db_subnet_1.id , aws_subnet.db_subnet_2.id]
  tags = {
    Name = "${var.vpc_name}-db-subnet-group"
  }
}
# Security group for EC2 (App tier)
resource "aws_security_group" "app_sg" {
  name        = "app_sg"
  description = "Security group for the EC2 app tier"
  vpc_id      = aws_vpc.main.id

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
  }

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # You can restrict this to specific ranges if needed
  }
}

#elb security group
resource "aws_security_group" "elb_sg" {
  vpc_id = aws_vpc.main.id

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

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${var.vpc_name}-igw"
  }
}

# Routing Table
resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name = "${var.vpc_name}-main-route-table"
  }
}

# Route Table Association
resource "aws_route_table_association" "web_subnet_1" {
  subnet_id      = aws_subnet.web_subnet_1.id
  route_table_id = aws_route_table.main.id
}

resource "aws_route_table_association" "web_subnet_2" {
  subnet_id      = aws_subnet.web_subnet_2.id
  route_table_id = aws_route_table.main.id
}

# Security Groups
resource "aws_security_group" "web_subnet_1sg" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${var.vpc_name}-web_subnet_1sg"
  }
}

resource "aws_security_group" "web_subnet_2sg" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${var.vpc_name}-web_subnet_2sg"
  }
}
resource "aws_security_group" "db_sg" {
  vpc_id = aws_vpc.main.id
egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
  }

  ingress {
    from_port   = 3306  # MySQL port (adjust if you're using another database)
    to_port     = 3306
    protocol    = "tcp"
    security_groups = [aws_security_group.app_sg.id]  # Allow traffic from EC2's app_sg
  }

  
  tags = {
    Name = "${var.vpc_name}-db_sg"
  }
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "subnet_1" {
  value = aws_subnet.web_subnet_1.id
}

output "subnet_2" {
  value = aws_subnet.web_subnet_2.id
}

output "private_subnet_1" {
  value = aws_subnet.app_subnet_1.id
}

output "private_subnet_2" {
  value = aws_subnet.app_subnet_2.id
}
output "db_subnet_1" {
  value = aws_subnet.db_subnet_1.id
}

output "db_subnet_2" {
  value = aws_subnet.db_subnet_2.id
}


output "subnet_1_security_group_id" {
  value = aws_security_group.web_subnet_1sg.id
}

output "subnet_2_security_group_id" {
  value = aws_security_group.web_subnet_2sg.id
}
output "elb_sg" {
  value = aws_security_group.elb_sg
}

output "app_sg" {
  value = aws_security_group.app_sg
}
output "db_sg" {
  value = aws_security_group.db_sg
}
output "db_subnet_group" {
  value = aws_db_subnet_group.db_subnet_group
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
}

variable "web_subnet_1_cidr" {
  description = "CIDR block for the subnet_1"
  type        = string
}

variable "web_subnet_2_cidr" {
  description = "CIDR block for the subnet_2"
  type        = string
}
variable "app_subnet_1_cidr" {
  description = "CIDR block for the app subnet_1"
  type        = string
}

variable "app_subnet_2_cidr" {
  description = "CIDR block for the app subnet_2"
  type        = string
}

variable "db_subnet_1_cidr" {
  description = "CIDR block for the db subnet_1"
  type        = string
}
variable "db_subnet_2_cidr" {
  description = "CIDR block for the db subnet_2"
  type        = string
}

variable "subnet_1_az" {
  description = "Availability zone for subnet_1"
  type        = string
}

variable "subnet_2_az" {
  description = "Availability zone for subnet_2"
  type        = string
