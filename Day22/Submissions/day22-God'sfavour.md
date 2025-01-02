### Name: God'sfavour Braimah
# Day 21: Putting It All Together - Terraform 30-Day Challenge 🎉
### Time: 12:50pm

# Putting It All Together - Terraform 30-Day Challenge 🎉

## Overview  
Day 22 marks the completion of *"Terraform: Up & Running"*. The focus today was on integrating workflows for deploying both **application code** and **infrastructure code** using Terraform, version control, and CI/CD practices. 

## Key Highlights  
- **Version Control:** Utilized Git for managing both application and infrastructure code.  
- **Terraform Cloud:** Connected VCS to Terraform Cloud for streamlined deployments and approval checks.  
- **Sentinel Policies:** Implemented compliance and security policies.  
- **CI/CD Integration:** Automated testing and deployments with a pipeline.  
- **Immutable Artifacts:** Promoted secure, versioned artifacts across environments.  

## Directory Structure  
```plaintext
project/
├── application/
│   ├── src/
│   │   └── app.py
│   └── Dockerfile
├── infrastructure/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── sentinel/
    └── allowed-providers.sentinel

## main.tf

```
terraform {
  cloud {
    organization = "your-organization"
    workspaces {
      name = "infrastructure-dev"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidr
  availability_zone = "${var.aws_region}a"

  tags = {
    Name        = "${var.environment}-private"
    Environment = var.environment
  }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnet_cidr
  availability_zone = "${var.aws_region}b"
  map_public_ip_on_launch = true

  tags = {
    Name        = "${var.environment}-public"
    Environment = var.environment
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = "${var.environment}-igw"
    Environment = var.environment
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name        = "${var.environment}-public-rt"
    Environment = var.environment
  }
}
```


   ### Variable.tf
```
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "private_subnet_cidr" {
  description = "CIDR block for private subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.0.2.0/24"
}
```
 ### Sentinel Policy
```
import "tfplan/v2" as tfplan

main = rule {
    all tfplan.resource_changes as _, rc {
        rc.provider_name in ["registry.terraform.io/hashicorp/aws"]
    }
}
```