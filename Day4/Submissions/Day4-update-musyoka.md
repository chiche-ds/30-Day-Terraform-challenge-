# Day 4: Mastering Basic Infrastructure with Terraform

## Participant Details
- **Name:** Musyoka Kilonzo
- **Task Completed:** Deploy a configurable and clustered web servers.
- **Date and Time:** 2024-08-24 12:00PM

# Terraform Code - Deploying a Configurable Web Server
### main.tf
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
}
#Retrieve the list of AZs in the current AWS region

data "aws_availability_zones" "available" {}
data "aws_region" "current" {}

#Define the VPC
resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name        = var.vpc_name
    Environment = "dev_environment"
    Terraform   = "true"
    Region      = data.aws_region.current.name
  }
}

#Deploy the private subnets

resource "aws_subnet" "private_subnets" {
  for_each   = var.private_subnets
  vpc_id     = aws_vpc.vpc.id
  cidr_block = cidrsubnet(var.vpc_cidr, 8, each.value)
  availability_zone = tolist(data.aws_availability_zones.available.names)[each.value]
  tags = {
    Name      = each.key
    Terraform = "true"
  }
}
#Deploy the public subnets
resource "aws_subnet" "public_subnets" {
  for_each   = var.public_subnets
  vpc_id     = aws_vpc.vpc.id
  cidr_block = cidrsubnet(var.vpc_cidr, 8, each.value + 100)
  availability_zone = tolist(data.aws_availability_zones.available.names)[each.value]
  map_public_ip_on_launch = true
  tags = {
    Name      = each.key
    Terraform = "true"
  }
}

#Create route tables for public and private subnets
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id ## Attach internet gw to the public RT

  }
  tags = {
    Name        = "Musyoka_public_rtb"
    Terraform   = "true"
    Environment = "Dev"
  }
}
resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway.id ## Attach NAT gw to the private RT
  }
  tags = {
    Name      = "musyoka_private_rtb"
    Terraform = "true"
  }
}

#Create route table associations

resource "aws_route_table_association" "public" {
  depends_on     = [aws_subnet.public_subnets]
  route_table_id = aws_route_table.public_route_table.id
  for_each       = aws_subnet.public_subnets
  subnet_id      = each.value.id
}
resource "aws_route_table_association" "private" {
  depends_on     = [aws_subnet.private_subnets]
  route_table_id = aws_route_table.private_route_table.id
  for_each       = aws_subnet.private_subnets
  subnet_id      = each.value.id
}

#Create Internet Gateway
resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "musyoka_igw"
  }
}
#Create EIP for NAT Gateway
resource "aws_eip" "nat_gateway_eip" {
  domain     = "vpc"
  depends_on = [aws_internet_gateway.internet_gateway]
  tags = {
    Name = "musyoka_igw_eip"
  }
}
#Create NAT Gateway
resource "aws_nat_gateway" "nat_gateway" {
  depends_on    = [aws_subnet.public_subnets]
  allocation_id = aws_eip.nat_gateway_eip.id
  subnet_id     = aws_subnet.public_subnets["musyoka-public_subnet-1"].id
  tags = {
    Name = "musyoka_nat_gateway"
  }
}

# Deploy a configurable web server

resource "aws_instance" "web-server" {
  ami               = var.image_id
  instance_type     = var.instance_type
  key_name          = var.key_name
  availability_zone = "us-east-1a"
  vpc_security_group_ids = [aws_security_group.web-server-sg.id]
  user_data = filebase64("userdata.sh")          
  user_data_replace_on_change = true
  
  tags = {
    Name = "web-server"
  }
}
# security group to allow http and ssh protocols

resource "aws_security_group" "web-server-sg" {
  name = "web-server-sg"
  vpc_id = aws_vpc.vpc.id
 ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = var.server_port
    to_port     = var.server_port
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
### variables.tf

```hcl
variable "aws_region" {
  type    = string
  default = "us-east-1"
}
variable "vpc_name" {
  type    = string
  default = "musyoka-vpc"
}
variable "vpc_cidr" {
  type    = string
  default = "10.240.0.0/16"
}
variable "private_subnets" {
  default = {
    "musyoka-private_subnet-1" = 1
    "musyoka-private_subnet_2" = 2
    "musyoka-private_subnet-3" = 3
  }
}
variable "public_subnets" {
  default = {
    "musyoka-public_subnet-1" = 1
    "musyoka-public_subnet-2" = 2
    "musyoka-public_subnet-3" = 3
  }
}
variable "server_port" {
  description = "The port the server will use for HTTP requests"
  type        = number
  default     = 80
}
variable "key_name" {
  description = "ssh key used to login to the EC2"
  default     = "musyoka"
}
variable "image_id" {
  default = "ami-04a81a99f5ec58529"
}
variable "instance_type" {
  default = "t2.micro"

}
```
### userdata.sh
```hcl
#!/bin/bash
                sudo apt-get update
                sudo apt-get install -y nginx
                # Modify the Nginx configuration to listen on port 8080
                #sed -i 's/listen       80;/listen       ${var.server_port};/g' /etc/nginx/nginx.conf
                sudo systemctl start nginx
                sudo systemctl enable nginx
```

# Terraform Code - Deploying clustered Web Servers

### main.tf

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
}
#Retrieve the list of AZs in the current AWS region

data "aws_availability_zones" "available" {}
data "aws_region" "current" {}

#Define the VPC
resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name        = var.vpc_name
    Environment = "dev_environment"
    Terraform   = "true"
    Region      = data.aws_region.current.name
  }
}

#Deploy the private subnets

resource "aws_subnet" "private_subnets" {
  for_each   = var.private_subnets
  vpc_id     = aws_vpc.vpc.id
  cidr_block = cidrsubnet(var.vpc_cidr, 8, each.value)
  availability_zone = tolist(data.aws_availability_zones.available.names)[each.value]
  tags = {
    Name      = each.key
    Terraform = "true"
  }
}
#Deploy the public subnets
resource "aws_subnet" "public_subnets" {
  for_each   = var.public_subnets
  vpc_id     = aws_vpc.vpc.id
  cidr_block = cidrsubnet(var.vpc_cidr, 8, each.value + 100)
  availability_zone = tolist(data.aws_availability_zones.available.names)[each.value]
  map_public_ip_on_launch = true
  tags = {
    Name      = each.key
    Terraform = "true"
  }
}

#Create route tables for public and private subnets
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id ## Attach internet gw to the public RT

  }
  tags = {
    Name        = "Musyoka_public_rtb"
    Terraform   = "true"
    Environment = "Dev"
  }
}



resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway.id ## Attach NAT gw to the private RT
  }
  tags = {
    Name      = "musyoka_private_rtb"
    Terraform = "true"
  }
}

#Create route table associations

resource "aws_route_table_association" "public" {
  depends_on     = [aws_subnet.public_subnets]
  route_table_id = aws_route_table.public_route_table.id
  for_each       = aws_subnet.public_subnets
  subnet_id      = each.value.id
}
resource "aws_route_table_association" "private" {
  depends_on     = [aws_subnet.private_subnets]
  route_table_id = aws_route_table.private_route_table.id
  for_each       = aws_subnet.private_subnets
  subnet_id      = each.value.id
}

#Create Internet Gateway
resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "musyoka_igw"
  }
}
#Create EIP for NAT Gateway
resource "aws_eip" "nat_gateway_eip" {
  domain     = "vpc"
  depends_on = [aws_internet_gateway.internet_gateway]
  tags = {
    Name = "musyoka_igw_eip"
  }
}
#Create NAT Gateway
resource "aws_nat_gateway" "nat_gateway" {
  depends_on    = [aws_subnet.public_subnets]
  allocation_id = aws_eip.nat_gateway_eip.id
  subnet_id     = aws_subnet.public_subnets["musyoka-public_subnet-1"].id
  tags = {
    Name = "musyoka_nat_gateway"
  }
}
# security group to allow http and ssh protocols

resource "aws_security_group" "web-server-sg" {
  name = "web-server-sg"
  vpc_id = aws_vpc.vpc.id
 ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = var.server_port
    to_port     = var.server_port
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

# Deploy a clustered web server
## The first step in creating an ASG is to create a launch configuration, which speci‐fies how to configure each EC2 Instance in the ASG

resource "aws_launch_configuration" "clustered-servers" {
 image_id = var.image_id
 instance_type = var.instance_type
 security_groups = [aws_security_group.web-server-sg.id]
 user_data = filebase64("userdata.sh")
 lifecycle {
   create_before_destroy = true
 }
}

# Now you can create the ASG itself using the aws_autoscaling_group resource:
resource "aws_autoscaling_group" "clustered-servers" {
  launch_configuration = aws_launch_configuration.clustered-servers.name
  vpc_zone_identifier = tolist([for subnet in aws_subnet.public_subnets : subnet.id])
  min_size = 2
  max_size = 5
  tag {
    key = "name"
    value = "musyoka-clustered-servers-asg"
    propagate_at_launch = true
  } 
}
```
### Reuse the variables and userdat.sh code of the configurable web server code
Below is my Architecture of the above deployment.

![AWS VPC Architecture](vpc-architecture.drawio%20(1).png)





