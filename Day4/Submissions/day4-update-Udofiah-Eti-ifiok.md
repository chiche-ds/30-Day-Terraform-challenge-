Use Terraform to deploy a configurable web server (main.tf)


# Provider Configuration
provider "aws" {
  region = var.aws_region
}

# Security Group to Allow Web Traffic
resource "aws_security_group" "web_sg" {
  name_prefix = "web-server-sg-"

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
    Name = "Web Server Security Group"
  }
}

# Key Pair (For SSH Access)
resource "aws_key_pair" "web_key" {
  key_name   = var.key_name
  public_key = var.public_key
}

# EC2 Instance
resource "aws_instance" "web_server" {
  ami           = var.ami_id # Example: Amazon Linux 2 AMI
  instance_type = var.instance_type
  key_name      = aws_key_pair.web_key.key_name
  security_groups = [aws_security_group.web_sg.name]

  # Configure the Web Server
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y httpd
              echo "<html><body><h1>Hello from Terraform Configurable Web Server</h1></body></html>" > /var/www/html/index.html
              sudo systemctl start httpd
              sudo systemctl enable httpd
              EOF

  tags = {
    Name = var.instance_name
  }
}

# Output the Public IP Address
output "web_server_public_ip" {
  description = "Public IP address of the web server"
  value       = aws_instance.web_server.public_ip
}



Use Terraform to deploy a configurable web server (variables.tf)


# AWS Region
variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

# Instance Type
variable "instance_type" {
  description = "Type of instance to deploy"
  type        = string
  default     = "t2.micro"
}

# Amazon Machine Image (AMI) ID
variable "ami_id" {
  description = "The AMI ID for the instance"
  type        = string
  default     = "ami-0c55b159cbfafe1f0" # Amazon Linux 2 in us-east-1
}

# Instance Name
variable "instance_name" {
  description = "The name of the web server instance"
  type        = string
  default     = "configurable-web-server"
}

# Key Pair Name
variable "key_name" {
  description = "Name of the key pair to use for SSH access"
  type        = string
}

# Public Key Content
variable "public_key" {
  description = "Public key to use for the key pair"
  type        = string
}




# web cluster (variable.tf)
variable "region" {
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}

variable "availability_zones" {
  description = "List of availability zones"
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "subnets_cidrs" {
  description = "CIDR blocks for subnets in each availability zone"
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "instance_type" {
  description = "Type of EC2 instance"
  default     = "t2.micro"
}

variable "ami_id" {
  description = "AMI ID for the web server"
  default     = "ami-12345678" # Replace with a valid AMI ID for your region
}

variable "key_name" {
  description = "Name of the key pair to access instances"
  default     = "my-key-pair" # Replace with your key pair



# web cluster (main.tf)
provider "aws" {
  region = var.region
}

# Create a VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "ClusteredVPC"
  }
}

# Create an Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "ClusteredIGW"
  }
}

# Create a public route table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "PublicRouteTable"
  }
}

# Add a default route to the internet gateway
resource "aws_route" "internet_access" {
  route_table_id         = aws_route_table.public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

# Create subnets in each availability zone
resource "aws_subnet" "clustered_subnets" {
  for_each = toset(var.availability_zones)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.subnets_cidrs[lookup(keys(var.availability_zones), each.key)]
  availability_zone       = each.value
  map_public_ip_on_launch = true

  tags = {
    Name = "Subnet-${each.key}"
  }
}

# Associate public route table with each subnet
resource "aws_route_table_association" "public_assoc" {
  for_each       = aws_subnet.clustered_subnets
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public_rt.id
}

# Create Security Group for Web Servers
resource "aws_security_group" "web_sg" {
  vpc_id = aws_vpc.main.id

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

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "WebServerSG"
  }
}

# Launch an EC2 instance in each subnet
resource "aws_instance" "web_servers" {
  for_each                    = aws_subnet.clustered_subnets
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = var.key_name
  subnet_id                   = each.value.id
  security_groups             = [aws_security_group.web_sg.name]
  associate_public_ip_address = true

  tags = {
    Name = "WebServer-${each.key}"
  }
}

# Output public IPs for web servers
output "web_server_ips" {
  description = "Public IP addresses of web servers"
  value       = [for server in aws_instance.web_servers : server.public_ip]
}

