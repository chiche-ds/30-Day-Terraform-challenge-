### Name: God'sfavour Braimah
### Task: Day 16: Working with Multiple Providers Part 2
### Date: 12/26/24
### Time: 7:20am
# Day 16: Production-Grade EKS Infrastructure with Terraform

## Overview
This repository contains a production-grade AWS EKS infrastructure implementation, created as part of the Terraform 30-Day Challenge (Day 16). The infrastructure follows best practices for modularity, testability, and maintainability.

## Features

- **Modular Design**: Infrastructure broken down into reusable modules
- **Multi-Environment Support**: Separate configurations for development and production
- **Infrastructure as Code Best Practices**: Version-controlled, testable infrastructure
- **Security-First Approach**: IAM roles with least privilege, secure networking

## Architecture Components

### Networking Module
- VPC with public and private subnets
- NAT Gateways for private subnet connectivity
- Configurable Availability Zones
- Security Groups and Route Tables

### IAM Module
- EKS Cluster IAM Role
- Node Group IAM Role
- Optional IRSA (IAM Roles for Service Accounts) support

### EKS Module
- Managed EKS Cluster
- Configurable Node Groups
- Supports both Spot and On-Demand instances
- Customizable scaling configuration

## Project Structure
 ├── environments/ │ ├── dev/ │ │ ├── main.tf # Dev environment configuration │ │ ├── variables.tf # Dev-specific variables │ │ └── terraform.tfvars │ └── prod/ # Production environment setup ├── modules/ │ ├── networking/ # VPC and subnet configurations │ ├── eks/ # EKS cluster and node groups │ └── iam/ # IAM roles and policies └── test/ # Infrastructure tests

 ```
  provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = "dev"
      Project     = var.project_name
      ManagedBy   = "terraform"
    }
  }
}

locals {
  cluster_name = "${var.project_name}-${var.environment}"
}

module "networking" {
  source = "../../modules/networking"

  environment   = var.environment
  vpc_cidr      = var.vpc_cidr
  az_count      = var.az_count
  cluster_name  = local.cluster_name
  tags          = var.tags
}

module "iam" {
  source = "../../modules/iam"

  cluster_name = local.cluster_name
  enable_irsa  = var.enable_irsa
  tags         = var.tags
  
}

module "eks" {
  source = "../../modules/eks"

  cluster_name            = local.cluster_name
  cluster_role_arn       = module.iam.cluster_role_arn
  node_role_arn          = module.iam.node_role_arn
  private_subnet_ids     = module.networking.private_subnet_ids
  public_subnet_ids      = module.networking.public_subnet_ids
  vpc_id                 = module.networking.vpc_id
  kubernetes_version     = var.kubernetes_version
  node_instance_types    = var.node_instance_types
  node_group_min_size    = var.node_group_min_size
  node_group_max_size    = var.node_group_max_size
  node_group_desired_size = var.node_group_desired_size
  capacity_type         = var.capacity_type
  tags                  = var.tags
}
```