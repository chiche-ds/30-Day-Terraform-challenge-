# Day 16: Building Production-Grade Infrastructure
## Participant Details

- **Name:** Dwayne Chima
- **Task Completed:** Refactored terraform code to be used in production-grade standards.
- **Date and Time:** 17th Dec 2024 09:31 AM

### Terraform directory
```
├── main.tf
├── modules
│   ├── cluster # Module for deploying instance cluster
│   │   ├── alb
│   │   │   ├── main.tf
│   │   │   ├── outputs.tf
│   │   │   └── vars.tf
│   │   └── autoscaling
│   │       ├── main.tf
│   │       ├── output.tf
│   │       └── vars.tf
│   ├── instance # Module for deploying instances
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   └── vars.tf
│   ├── k8 # Module for deploying EKS Cluster
│   │   ├── iam
│   │   │   ├── iam.tf
│   │   │   └── outputs.tf
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   └── vars.tf
│   ├── secrets # Module for retrieving SSM secrets
│   │   ├── main.tf
│   │   └── outputs.tf
│   ├── security_groups # Module for deploying Security Groups
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   └── vars.tf
│   ├── tls # Module for creating ssh key
│   │   ├── main.tf
│   │   ├── output.tf
│   │   └── vars.tf
│   └── vpc # Module for Deploying a VPC
│       ├── main.tf
│       ├── output.tf
│       └── vars.tf
├── outputs.tf
├── templates # Folder for template files 
│   └── user_data.sh
├── terraform.tf
└── vars.tf
```
## Architecture Diagram
![directory](https://github.com/user-attachments/assets/0a6d67cd-9ba5-4757-aed0-efcc3488c65f)

## Terraform code
### terraform.tf
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.80.0"
    }

    tls = {
      source  = "hashicorp/tls"
      version = ">= 4.0.6"
    }

    local = {
      source  = "hashicorp/local"
      version = ">= 2.5.2"
    }
  }


  backend "s3" {
    bucket = "terraform-state-bucket"
    key    = "terraform/"
    region = "us-east-1"
  }

   required_version = ">= 1.10.0"
}

provider "aws" {
  region = "us-east-1"
  alias  = "east"
}

provider "aws" {
  region = "us-west-2"
  alias  = "west"
}
```

### main.tf
```hcl
module "vpc" {
  source = "./modules/vpc"

  providers = {
    aws = aws.east
  }
}

module "tls" {
  source    = "./modules/tls"
  key_name  = "aws"
  file_path = "${path.module}/aws.pem"
}

module "security_groups" {
  source                        = "./modules/security_groups"
  vpc_id                        = module.vpc.vpc_id
  inbound_ports                 = var.inbound_ports
  create_alb_ref_security_group = false
  providers = {
    aws = aws.east
  }
}

module "instance" {
  source = "./modules/instance"
  web_sg = module.security_groups.web_sg
  public_subnets = module.vpc.public_subnets
  secret_data = module.secrets.secrets
  providers = {
    aws = aws.east
  }
}
```

### vars.tf
```hcl
variable "tag" {
  type    = string
  default = "webserver"
}


variable "inbound_ports" {
  description = "This is the ports open for inbound trafic"
  type        = list(string)
  default     = ["80"]
}

variable "distro_version" {
  type    = string
  default = "24.04"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}
```

***
***

### modules/vpc
```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}


resource "aws_vpc" "vpc" {
  cidr_block       = var.cidr
  instance_tenancy = "default"
  tags = {
    Name = "${var.tag}-vpc"
  }
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "${var.tag}-igw"
  }
}

data "aws_availability_zones" "available" {}


resource "aws_subnet" "private_subnets" {
  count                   = var.public_subnets_no
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = cidrsubnet(var.cidr, 8, count.index)
  availability_zone       = tolist(data.aws_availability_zones.available.names)[count.index]
  map_public_ip_on_launch = false
  tags = {
    Name = "${var.tag}-private-subent-${count.index}"
  }
}

resource "aws_subnet" "public_subnets" {
  count                   = var.public_subnets_no
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = cidrsubnet(var.cidr, 8, count.index + 100)
  availability_zone       = tolist(data.aws_availability_zones.available.names)[count.index]
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.tag}-public-subent-${count.index}"
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
```

### modules/security_groups
```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

resource "aws_security_group" "web_sg" {
  name        = "web_sg"
  description = "Allow TLS traffic inbound and all outbound"
  vpc_id      = var.vpc_id
  tags = {
    Name = "${var.tag}-sg"
  }
}

# Conditional creation of ingress rule
resource "aws_vpc_security_group_ingress_rule" "allow_http" {
  for_each = { for idx, port in var.inbound_ports : idx => port }

  security_group_id         = aws_security_group.web_sg.id
  from_port                 = each.value
  to_port                   = each.value
  ip_protocol               = "tcp"
  
  # Conditionally set referenced_security_group_id
  referenced_security_group_id = var.create_alb_ref_security_group ? var.alb_sg.id : null
  
  
  # Conditionally set cidr_blocks
  cidr_ipv4 = var.create_alb_ref_security_group ? null : "0.0.0.0/0"
}


# Conditional creation of egress rule
resource "aws_vpc_security_group_egress_rule" "app_allow_all_outbound" {
  security_group_id = aws_security_group.web_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}
```

### modules/tls
```hcl
resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "aws_key_pair" "key_pair" {
  key_name   = var.key_name
  public_key = tls_private_key.ssh_key.public_key_openssh
}

resource "local_file" "private_key" {
  content  = tls_private_key.ssh_key.private_key_pem
  filename = var.file_path

  provisioner "local-exec" {
    command = "chmod 600 ${local_file.private_key.filename}"
  }
}
```

### modules/instance
```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd*/ubuntu-*-${var.distro_version}-amd64-server-*"]
  }

  owners = ["099720109477"]
}

data "aws_ec2_instance_type" "instance" {
  instance_type = var.instance_type
}

resource "aws_instance" "web_server" {
  instance_type          = var.instance_type
  ami                    = data.aws_ami.ubuntu.id
  subnet_id              = var.public_subnets[0].id
  vpc_security_group_ids = [var.web_sg.id]
  key_name               = var.ssh_key != null ? var.ssh_key.key_name : null

  user_data = <<-EOT
    #!/bin/bash
    sudo apt update -y
    sudo apt upgrade -y
    sudo apt install -y nginx
    sudo systemctl start nginx
    sudo systemctl enable nginx
    echo "<h1>Hello from ${var.secret_data.hello_text}</h1>" | sudo tee /var/www/html/index.html
  EOT

  lifecycle {
    precondition {
      condition = (
        data.aws_ec2_instance_type.instance.free_tier_eligible ||
        var.instance_type == "t2.small"
      ) && data.aws_ec2_instance_type.instance.ebs_optimized

      error_message = "Instance must be part of Free tier, or 't2.small', and must be EBS optimized."
    }
  }
}
```



