# Day 4: Mastering Basic Infrastructure with Terraform

## Participant Details

- **Name:** Duncan Gaturu
- **Task Completed:** Deploying Basic Infrastructure with Terraform
- **Date and Time:** 2024-08-26 at 10:00 pm

## Terraform Code 

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# creating a VPC


resource "aws_vpc" "dha-vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "production"
  }
}

# Create Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.dha-vpc.id
}


# Create Custom Route Table


resource "aws_route_table" "dha-route-table" {
  vpc_id = aws_vpc.dha-vpc.id


  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }


  route {
    ipv6_cidr_block        = "::/0"
    gateway_id = aws_internet_gateway.gw.id
  }


  tags = {
    Name = "production"
  }
}

# Create a subnet

resource "aws_subnet" "subnet-1" {
  vpc_id = aws_vpc.dha-vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "us-east-1a"


  tags = {
    Name = "production-subnet"
  }
}

# Associate subnet with Route Table


resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet-1.id
  route_table_id = aws_route_table.dha-route-table.id
}


# Create Security Group to allow port 22,80,443


resource "aws_security_group" "allow_web" {
  name        = "allow_web_traffic"
  description = "Allow Web inbound traffic"
  vpc_id      = aws_vpc.dha-vpc.id
  ingress {
    description = "HTTPS TRAFFIC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "HTTP TRAFFIC"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "SSH TRAFFIC"
    from_port   = 2
    to_port     = 2
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
    Name = "allow_Web"
  }
}

# Create a network interface with ip in the subnet that was created in step 4

resource "aws_network_interface" "web_server_nic" {
  subnet_id       = aws_subnet.subnet-1.id
  private_ips     = ["10.0.1.50"]
  security_groups = [aws_security_group.allow_web.id]
}


# Assign an elastic ip to network interface created in step 7

resource "aws_eip" "lb" {
  domain   = "vpc"
  network_interface         = aws_network_interface.web_server_nic.id
  associate_with_private_ip = "10.0.1.50"
  depends_on = [ aws_internet_gateway.gw ]
}


# Create Ubuntu servers and install/enable apache

resource "aws_instance" "web-server-instance" {
  ami = "ami-0e86e20dae9224db8"
  instance_type = "t2.micro"
  availability_zone = "us-east-1a"
 
  network_interface {
    device_index = 0
    network_interface_id = aws_network_interface.web_server_nic.id
  }

  tags = {
    Name = "WebServer"
  }
}
 


