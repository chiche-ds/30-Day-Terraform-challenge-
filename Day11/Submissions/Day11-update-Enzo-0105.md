# Day 11: Terraform Conditionals

## Participant Details

- **Name:** Salako Lateef
- **Task Completed:** Modify Existing Code:
- **Date and Time:** 2024-10-03 10:14 AM 
## main.tf
```
provider "aws" {
  region = var.region
}

data "aws_ami" "web" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["ubuntu/*"]
  }
}

locals {
  name = "web-server"
  Terraform = "true"
  Environment = var.env 
}

locals {
  common_tags = {
    Name = local.name
    Terraform = local.Terraform
    Environment = local.Environment
  }
}
#Vpc creation for our application Network
resource "aws_vpc" "vpc" {
  cidr_block = var.vpc

  tags = {
    Name      = "Web-server-vpc"
    Terraform = "Yes"
  }
}

#public Subnet creation
resource "aws_subnet" "public-sub" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.public-cidr
  availability_zone = "us-east-1a"

  tags = {
    Name      = "web-server-public-sub"
    Terraform = "yes"
  }
}
resource "aws_subnet" "public-sub1" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.public-cidr1
  availability_zone = "us-east-1b"

  tags = {
    Name      = "web-server-public-sub1"
    Terraform = "yes"
  }
}

#private subnet creation 
resource "aws_subnet" "private-sub" {
  vpc_id     = aws_vpc.vpc.id
  cidr_block = var.private-cidr

  tags = {
    Name      = "web-server-private-subnet"
    Terraform = "yes"
  }
}

#Internet gateway for vpc
resource "aws_internet_gateway" "web-igw" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name      = "web-igw"
    Terraform = "yes"
  }
}

#Route table for vpc
resource "aws_route_table" "web-rt" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.web-igw.id
  }
}

#associating the public subnet
resource "aws_route_table_association" "rt-ass" {
  subnet_id      = aws_subnet.public-sub.id
  route_table_id = aws_route_table.web-rt.id
}

resource "aws_route_table_association" "rt-assoc" {
  subnet_id      = aws_subnet.public-sub1.id
  route_table_id = aws_route_table.web-rt.id
}

resource "aws_route_table" "private-web-rt" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name      = "private-web-rt"
    Terraform = "yes"
  }
}

#associating the public subnet
resource "aws_route_table_association" "rt-asso" {
  subnet_id      = aws_subnet.private-sub.id
  route_table_id = aws_route_table.private-web-rt.id
}

#Creating a security group
resource "aws_security_group" "web-sg" {
  name   = "web-sg"
  vpc_id = aws_vpc.vpc.id
  ingress {
    from_port   = "80"
    to_port     = "80"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = "22"
    to_port     = "22"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = "0"
    to_port     = "0"
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web-server" {
  count = var.env == dev ? 2 : 0 
  ami             = data.aws_ami.web.id
  subnet_id       = aws_subnet.public-sub.id
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.web-sec.id]
  associate_public_ip_address = "true"

  user_data = <<-EOF
  #!/bin/bash 
  sudo apt update -y
  sudo apt install apache2 -y 
  sudo systemctl start apache2 
  EOF

  tags = {
    Name = local.type
  }
```
## variables.tf
```
variable "vpc-cidr" {
  type    = string
  default = "196.168.0.0/16"
}

variable "public-cidr" {
  type    = string
  default = "196.168.1.0/24"
}

variable "private-cidr" {
  type    = string
  default = "196.168.7.0/24"
}

variable "env" {
  type = string
  default = "prod"
  validation {
    condition = contains(["dev", "prod"], var.env)
    error_message = "input only dev or prod"
  }
}
```
