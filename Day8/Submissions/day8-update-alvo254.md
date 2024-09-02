# Day 8: Module Basics

## Participant Details

- **Name:** Alvin Ndungu
- **Task Completed:** Module Basics
- **Date and Time:** 2024-08-20 15:18pm

```
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region  = "us-east-1"
  profile = "default"
}


# -------------------------------------------------------main.tf-----------------------------------------------------------------
module "vpc" {
  source = "./modules/vpc"

}

//public instance 
module "ec2" {
  source         = "./modules/ec2"
  vpc_id         = module.vpc.vpc_id
  subnet         = module.vpc.public_subnet_az1_id
  security_group = module.sg.security_group_id
  subnet_2 = module.vpc.public_subnet_az2_id
}

module "sg" {
  source = "./modules/sg"
  vpc_id = module.vpc.vpc_id

}

# -------------------------------------------------------end of main.tf-----------------------------------------------------------------



# -------------------------------------------------------vpc module [modules/vpc]-----------------------------------------------------------------
variable "vpc_cidr_notation" {
  type = string
  description = "Ip range for the cidr"
  default = "10.5.0.0/16"
}

variable "project" {
  default = "toast"
}

variable "environment" {
    type = string
    description = "Environment"
    default = "Dev"
}


variable "region" {
    default = "us-east-1"
}

variable "public_subnet" {
  default = "10.5.5.0/24"
}

variable "public_subet_2" {
  default = "10.5.10.0/24"
}


variable "private_subnet"{
  default = "10.5.20.0/24"
    
}

variable "private_subnet_2"{
   default = "10.5.30.0/24"
    
}

variable "private_data"{
  default = "10.5.40.0/24"

}

variable "private_data_2"{
     default = "10.5.50.0/24"
}

resource "aws_vpc" "vpc" {
  cidr_block           = var.vpc_cidr_notation
  //Tenancy defines how EC2 instances are distributed across physical hardware and affects pricing
  instance_tenancy     = "default"
  enable_dns_hostnames = true

  tags = {
    Name = "${var.project}-${var.environment}-vpc"
  }
}

data "aws_region" "current" {}

resource "aws_vpc_ipam" "pam" {
  operating_regions {
    region_name = data.aws_region.current.name
  }
}

resource "aws_vpc_ipv6_cidr_block_association" "ipv6" {
  ipv6_ipam_pool_id = aws_vpc_ipam_pool.ipv6.id
  vpc_id = aws_vpc.vpc.id
}


resource "aws_vpc_ipam_pool" "ipv6" {
  address_family = "ipv6"
  ipam_scope_id  = aws_vpc_ipam.pam.public_default_scope_id
  locale         = "us-east-1"
  description    = "public ipv6"

  aws_service    = "ec2"
}

# resource "aws_vpc_ipam_pool_cidr" "ipv6_test_public" {
#   ipam_pool_id = aws_vpc_ipam_pool.ipv6.id
#   cidr         = var.ipv6_cidr
#   cidr_authorization_context {
#     message   = var.message
#     signature = var.signature
#   }
# }

# create internet gateway and attach it to vpc
resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${var.project}-${var.environment}-igw"
  }
}

# use data source to get all avalablility zones in region
data "aws_availability_zones" "available_zones" {}

# create public subnet az1
resource "aws_subnet" "public_subnet_az1" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.public_subnet
  availability_zone       = data.aws_availability_zones.available_zones.names[0]  //this is indexing
  //resources launched with this will have a public ip address
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project}-${var.environment}-public-az1"
  }
}

# create public subnet az2
resource "aws_subnet" "public_subnet_az2" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.public_subet_2
  availability_zone       = data.aws_availability_zones.available_zones.names[1]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project}-${var.environment}-public-az2"
  }
}

# create route table and add public route
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
  }

  tags = {
    Name = "${var.project}-${var.environment}-public-rt"
  }
}

# associate public subnet az1 "public route table"
resource "aws_route_table_association" "public_subnet_az1_rt_association" {
  subnet_id      = aws_subnet.public_subnet_az1.id
  route_table_id = aws_route_table.public_route_table.id
}

# associate public subnet az2 to "public route table"
resource "aws_route_table_association" "public_subnet_2_rt_association" {
  subnet_id      = aws_subnet.public_subnet_az2.id
  route_table_id = aws_route_table.public_route_table.id
}

# create private app subnet az1
resource "aws_subnet" "private_app_subnet_az1" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.private_subnet
  availability_zone       = data.aws_availability_zones.available_zones.names[0]
  map_public_ip_on_launch = false

  tags = {
    Name = "${var.project}-${var.environment}-private-app-az1"
  }
}

# create private app subnet az2
resource "aws_subnet" "private_app_subnet_az2" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.private_subnet_2
  availability_zone       = data.aws_availability_zones.available_zones.names[1]
  map_public_ip_on_launch = false

  tags = {
    Name = "${var.project}-${var.environment}-private-app-az2"
  }
}

# create private data subnet az1
resource "aws_subnet" "private_data_subnet_az1" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.private_data
  availability_zone       = data.aws_availability_zones.available_zones.names[0]
  map_public_ip_on_launch = false

  tags = {
    Name = "${var.project}-${var.environment}-private-data-az1"
  }
}

# create private data subnet az2
resource "aws_subnet" "private_data_subnet_az2" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.private_data_2
  availability_zone       = data.aws_availability_zones.available_zones.names[1]
  map_public_ip_on_launch = false

  tags = {
    Name = "${var.project}-${var.environment}-private-data-az2"
  }
} 

output "region" {
  value = var.region
}

# export the project name
output "project" {
  value = var.project
}

# export the environment
output "environment" {
  value = var.environment
}

# export the vpc id
output "vpc_id" {
  value = aws_vpc.vpc.id
}

# export the internet gateway
output "internet_gateway" {
  value = aws_internet_gateway.internet_gateway.id
}

# export the public subnet az1 id
output "public_subnet_az1_id" {
  value = aws_subnet.public_subnet_az1.id
}

# export the public subnet az2 id
output "public_subnet_az2_id" {
  value = aws_subnet.public_subnet_az2.id
}

# export the private app subnet az1 id
output "private_app_subnet_az1_id" {
  value = aws_subnet.private_app_subnet_az1.id
}

# export the private app subnet az2 id
output "private_app_subnet_az2_id" {
  value = aws_subnet.private_app_subnet_az2.id
}

# export the private data subnet az1 id
output "private_data_subnet_az1_id" {
  value = aws_subnet.private_data_subnet_az1.id
}

# export the private data subnet az2 id
output "private_data_subnet_az2_id" {
  value = aws_subnet.private_data_subnet_az2.id
}

# export the first availability zone
output "availability_zone_1" {
  value = data.aws_availability_zones.available_zones.names[0]
}

# export the second availability zone
output "availability_zone_2" {
  value = data.aws_availability_zones.available_zones.names[1]
}

# -------------------------------------------------------end of vpc module-----------------------------------------------------------------



# -------------------------------------------------------sccurity group [module/sg]-----------------------------------------------------------------
variable "vpc_id" {
  type = string
  description = "Gets the vpc"
}

resource "aws_security_group" "alvo-toast" {
  name        = "alvo-toast"
  description = "my security group"
 
  vpc_id      = var.vpc_id

  ingress = [
    {
      description      = "HTTP"
      from_port        = 80
      to_port          = 80
      protocol         = "tcp"
      cidr_blocks      = ["0.0.0.0/0"]
      prefix_list_ids  = []
      security_groups  = []
      self             = false
      ipv6_cidr_blocks = []

  },
      {
      description      = "HTTS"
      from_port        = 443
      to_port          = 443
      protocol         = "tcp"
      cidr_blocks      = ["0.0.0.0/0"]
      prefix_list_ids  = []
      security_groups  = []
      self             = false
      ipv6_cidr_blocks = []

  },
  {
      description      = "SSH"
      from_port        = 22
      to_port          = 22
      protocol         = "tcp"
      //The /32 means use a single ip
      cidr_blocks      = ["105.163.158.30/32"] //Please change to your own IP address for this to work
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      security_groups  = []
      self             = false
  },
  ]

  egress = [
    {
      description      = "outgoing traffic"
      from_port        = 0
      to_port          = 0
      protocol         = "-1"
      cidr_blocks      = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
      prefix_list_ids  = []
      security_groups  = []
      self             = false

  }
  ]

  tags = {
    Name = "allow_toast_tls"
  }

}

output "security_group_id" {
    value = aws_security_group.alvo-toast.id
  
}
# -------------------------------------------------------end of sg group module-----------------------------------------------------------------



# -------------------------------------------------------EC2 instance [module/EC2]-----------------------------------------------------------------

variable "vpc_id" {
  type = string
  description = "Gets the vpc"
}


variable "subnet" {
  description = "subnet"
}

variable "security_group" {
  type = string
}

variable "subnet_2"{
  description = "subnet2"
}

resource "aws_instance" "alvo-toast" {
  ami = "ami-053b0d53c279acc90"
  instance_type = "t2.micro"
  
  subnet_id = var.subnet
  //This is interpolation or directive
  key_name = "${aws_key_pair.deployer.key_name}"

  user_data = data.template_file.user_data.rendered

  # 	user_data = <<EOF
	# 	#! /bin/bash
  #   sudo apt-get update
	# 	sudo apt install nginx
	# 	sudo systemctl start nginx
	# 	sudo systemctl enable nginx
	# EOF

  # vpc_security_group_ids = [aws_security_group.alvo-toast.id]
  vpc_security_group_ids = [var.security_group]


  tags = {
	Name = "alvin-toast"
  }
}


resource "aws_instance" "alvo-toast-2" {
  ami = "ami-053b0d53c279acc90"
  instance_type = "t2.micro"
  
  subnet_id = var.subnet_2
  //This is interpolation or directive
  key_name = "${aws_key_pair.deployer.key_name}"

  user_data = data.template_file.data_2.rendered


  # vpc_security_group_ids = [aws_security_group.alvo-toast.id]
  vpc_security_group_ids = [var.security_group]


  tags = {
	Name = "alvin-toast-2"
  }
}




resource "aws_key_pair" "deployer" {
  key_name = "deployer-key"
  //storing ssh key on the server
  public_key = tls_private_key.RSA.public_key_openssh
}


resource "tls_private_key" "RSA" {
  algorithm = "RSA"
  rsa_bits = 4096
}

resource "local_file" "alvo-ssh-keys" {
	# content = tls_private_key.RSA.private_key_pem
	content = tls_private_key.RSA.private_key_pem
	filename = "alvo-ssh-keys.pem"
}


data "template_file" "user_data" {
  template = file("${path.module}/install_nginx.sh")
}

data "template_file" "data_2" {
  template = file("${path.module}/do_stuff.sh")
}
# -------------------------------------------------------end of EC2 module-----------------------------------------------------------------
```