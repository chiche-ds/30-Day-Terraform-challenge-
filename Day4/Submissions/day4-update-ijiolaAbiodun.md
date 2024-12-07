# Day 4 Update - Ijiola Abiodun

## Date: December 4, 2024

### Task: Mastering Basic Infrastructure with Terraform

**Completed Task**:
- Today, I deployed a configurable and clustered web server using 
Terraform on AWS, incorporating resources such as VPC, subnets (both 
public and private), internet gateway, NAT gateway, load balancer, and 
auto-scaling. I explored Terraform's core concepts and utilized its 
providers, resource blocks, and workflow.

### Resources Deployed:
1. **Cloud Provider**: AWS
2. **Region**: `us-east-1`
3. **VPC**: Created a new VPC with a CIDR block of `10.0.0.0/16`.
4. **Subnets**: Deployed public and private subnets across multiple 
availability zones.
5. **Internet Gateway**: Added an internet gateway for public subnet 
access.
6. **NAT Gateway**: Created a NAT gateway for internet access from private 
subnets.
7. **Route Tables**: Configured route tables for both public and private 
subnets.
8. **Web Server Instances**: Deployed a clustered web server environment 
with two EC2 instances in the public subnets.
9. **Load Balancer**: Created an Application Load Balancer (ALB) to 
distribute traffic to the web servers.
10. **Auto Scaling**: Configured an Auto Scaling Group (ASG) to 
automatically scale the number of instances between 2 and 5.

### Key Terraform Code Sections:
```hcl
# Block for cloud provider
provider "aws" {
  region = "us-east-1"
}

# Define the VPC
resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name        = var.vpc_name
    Environment = "test_environment"
    Terraform   = "true"
  }
}

# Deploy the private subnets
resource "aws_subnet" "private_subnets" {
  for_each = var.private_subnets

  vpc_id            = aws_vpc.vpc.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, each.value)
  availability_zone = 
tolist(data.aws_availability_zones.available.names)[each.value]

  tags = {
    Name      = each.key
    Terraform = "true"
  }
}

# Deploy the public subnets
resource "aws_subnet" "public_subnets" {
  for_each = var.public_subnets

  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, each.value + 100)
  availability_zone       = 
tolist(data.aws_availability_zones.available.names)[each.value]
  map_public_ip_on_launch = true

  tags = {
    Name      = each.key
    Terraform = "true"
  }
}

# Add AWS Internet Gateway
resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name      = "internet_gateway"
    Terraform = "true"
  }
}

# Create Elastic IP for NAT Gateway
resource "aws_eip" "nat_gateway_eip" {
  domain = "vpc"

  tags = {
    Name = "nat_gateway_eip"
  }
}

# Create NAT Gateway
resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.nat_gateway_eip.id
  subnet_id     = aws_subnet.public_subnets["public_subnet_1"].id

  tags = {
    Name = "nat_gateway"
  }
}

# Creating a clustered Web Server
resource "aws_instance" "webserver" {
  count = 2
  ami = var.ami_id
  instance_type = var.instance_type
  subnet_id = aws_subnet.public_subnets["Public_subnet_1"].id

  tags = {
    Name = "WebServer-${count.index + 1}"
  }
}

# Creating an Application Load Balancer
resource "aws_lb" "app_load_balancer" {
  name = "web-alb"
  internal = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.lb_sg.id]
  subnets = values(aws_subnet.public_subnets)

  tags = {
    Name = "Web-ALB"
  }
}

# Creating Auto Scaling Group
resource "aws_autoscaling_group" "web_asg" {
  launch_configuration = aws_launch_configuration.web_lc.id
  min_size = 2
  max_size = 5
  vpc_zone_identifier = aws_subnet.public_subnets[*].id
}

