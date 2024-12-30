# Deploying Basic Infrastructure with Terraform

## Participant Details
* Name: Dwayne Chima
* Task Completed: Deploying Basic Infrastructure with Terraform
* Date and Time: 5th Dec 2024 5:00 AM
  
### Architecture Diagram

![archi](https://github.com/user-attachments/assets/5a6610d8-626c-473b-a255-1c5b0416357f)



### **providers.tf**
```
provider "aws" {
  region = "us-east-1"
}

```

### **main.tf***
```
resource "aws_vpc" "vpc" {
  cidr_block = var.cidr
  instance_tenancy = "default"
  tags = {
    Name = "${var.tag}-vpc"
  }
}

data "aws_availability_zones" "available" {}

resource "aws_subnet" "private_subnets" {
  count                   = var.public_subnets_no
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = cidrsubnet(var.cidr, 8, count.index) 
  availability_zone       = tolist(data.aws_availability_zones.available.names)[count.index]
  map_public_ip_on_launch = true
  tags                    = {
    Name = "${var.tag}-private-subent-${count.index}"
  }
}

resource "aws_subnet" "public_subnets" {
  count                   = var.public_subnets_no
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = cidrsubnet(var.cidr, 8, count.index + 100) 
  availability_zone       = tolist(data.aws_availability_zones.available.names)[count.index]
  map_public_ip_on_launch = true
  tags                    = {
    Name = "${var.tag}-public-subent-${count.index}"
  }
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "${var.tag}-igw"
  }
}

resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
  }

  tags = {
    Name = "${var.tag}-public-route-table"
  }
}

# Associate public subnets with the route table
resource "aws_route_table_association" "public_route_table_association" {
  depends_on     = [aws_subnet.public_subnets]
  route_table_id = aws_route_table.public_route_table.id
  for_each       = { for idx, subnet in aws_subnet.public_subnets : idx => subnet }
  subnet_id      = each.value.id
}


resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "${var.tag}-private-route-table"
  }
}

resource "aws_route_table_association" "private" {
  depends_on     = [aws_subnet.private_subnets]
  route_table_id = aws_route_table.private_route_table.id
  for_each       = { for idx, subnet in aws_subnet.private_subnets : idx => subnet }
  subnet_id      = each.value.id
}


# ..........................Security Groups................................. #

resource "aws_security_group" "web_sg" {
  name        = "web_sg"
  description = "Allow TLS traffic inbound and all outbound"
  vpc_id      = aws_vpc.vpc.id
  tags = {
    Name = "${var.tag}-sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_http" {
  for_each          = { for idx, port in var.inbound_ports : idx => port } 
  security_group_id = aws_security_group.web_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = each.value
  to_port           = each.value
  ip_protocol       = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "app_allow_all_outbound" {
  security_group_id = aws_security_group.web_sg.id
  cidr_ipv4         = "0.0.0.0/0"  
  ip_protocol       = "-1"         
}


# ..........................Web server................................. #

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd*/ubuntu-*-${var.distro_version}-amd64-server-*"]
  }

  owners = ["099720109477"]  
}

resource "aws_instance" "web_server" {
  instance_type          = var.instance_type
  ami                    = data.aws_ami.ubuntu.id
  subnet_id              = aws_subnet.public_subnets[0].id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  user_data = <<-EOT
    #!/bin/bash
    sudo apt update -y
    sudo apt upgrade -y
    sudo apt install -y nginx
    sudo systemctl start nginx
    sudo systemctl enable nginx
    echo "<h1>Hello from Terraform</h1>" | sudo tee /var/www/html/index.html
  EOT
}
```

### ***vars.tf***
```
variable "tag" {
  type = string
  default = "webserver"
}

variable "cidr" {
  description = "This is the Cidr block of he vpc"
  type = string
  default = "10.0.0.0/16"
}

variable "private_subnets_no" {
  description = "This is the number of Private subnets"
  type = number
  default = 1
}

variable "public_subnets_no" {
  description = "this is the numer of Public subnets"
  type = number
  default = 1
}

variable "inbound_ports" {
  description = "This is the ports open for inbound trafic"
  type = list(string)
  default = [ "80" ]
}

variable "distro_version" {
  type = string
  default = "24.04"
}

variable "instance_type" {
  type = string
  default = "t2.micro"
}
```

