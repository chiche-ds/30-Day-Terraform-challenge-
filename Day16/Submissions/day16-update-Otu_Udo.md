# Day 16: Building Production-Grade Infrastructure

## Participant Details

- **Name:** Otu Michael Udo
- **Task Completed:** Edited code to be production-grade ready
- **Date and Time:**27th December, 2024 | 5:16 PM

### Overview
Production level infra is scary. If I just joined a company I would not like if my code is used in production. I would not want to be the source of my company's download. But after this task, I felt a bit more confident about building things that can actually be used in production. best practices, security and proper documentation.
Provisioned a custom VPC for better control over networking configurations and scalability.
📦 Integrated an S3 backend to enhance state management for both staging and production.
🎯 Implemented Terraform namespaces for seamless staging and production environment management.
These updates ensure optimized resource allocation, improved scalability, and streamlined deployments across environments.

I got to understand that production grade code goes beyond just writing code that works. It encompasses a lot of different moving parts and involves a lot including versioning and testing.

## Terraform Code 
```hcl
terraform {
  required_version = ">= 1.0.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

# Get authentication credentials to interact with the EKS cluster
data "aws_eks_cluster_auth" "cluster" {
  name = module.eks_cluster.cluster_name
}

# Configure the Kubernetes provider to interact with the newly created EKS cluster
provider "kubernetes" {
  host                   = module.eks_cluster.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks_cluster.cluster_certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

# Create a custom VPC using the custom VPC module
module "vpc" {
  source = "C://Users//madus//Desktop//30 Days of Terraform//30-Day-Terraform-challenge-//Day16//vpc_module" 

  cidr_block        = "10.0.0.0/16"
  subnet_a_cidr     = "10.0.1.0/24"
  subnet_b_cidr     = "10.0.2.0/24"
  availability_zone_a = "us-east-1a"
  availability_zone_b = "us-east-1b"
}

# Create an EKS cluster using the custom VPC
module "eks_cluster" {
  source = "C://Users//madus//Desktop//30 Days of Terraform//30-Day-Terraform-challenge-//Day16//eks_cluster_module"

  name           = var.cluster_name
  min_size       = 1
  max_size       = 2
  desired_size   = 1
  instance_types = ["t3.small"]

  vpc_id          = module.vpc.vpc_id
  subnet_ids      = [module.vpc.subnet_a_id, module.vpc.subnet_b_id]
}

# Deploy a simple web application to the EKS cluster
module "simple_webapp" {
  source = "C://Users//madus//Desktop//30 Days of Terraform//30-Day-Terraform-challenge-//Day16//k8s_module"

  name           = var.app_name
  image          = "training/webapp"
  replicas       = 2
  container_port = 5000
  environment_variables = {
    PROVIDER = "Terraform"
  }
terraform {
  backend "s3" {
    bucket = "otu-bucket-state"
    key    = "project-${terraform.workspace}.tfstate"  # State file is separated by workspace
    region = "us-east-1"
    encrypt = true
    dynamodb_table = "state-lock"  # DynamoDB table for state locking
  }
}

  # Ensure the web app is deployed after the cluster is ready
  depends_on = [module.eks_cluster]
}

# Outputs
output "eks_cluster_endpoint" {
  value = module.eks_cluster.cluster_endpoint
}

output "eks_cluster_name" {
  value = module.eks_cluster.cluster_name
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

```



```