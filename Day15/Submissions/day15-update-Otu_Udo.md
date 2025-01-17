# Day 15: Working with Multiple Providers - Part 2

## Participant Details

- **Name:** Otu Michael Udo
- **Task Completed:** Working with multiple different providers. Integrating kubernetes providers with aws in terraform.
- **Date and Time:** 22nd December, 2024 | 10:34 PM

### Overview

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

# We need to authenticate to the EKS cluster, but only after it has been created. We accomplish this by using the
# aws_eks_cluster_auth data source and having it depend on an output of the eks-cluster module.

provider "kubernetes" {
  host = module.eks_cluster.cluster_endpoint
  cluster_ca_certificate = base64decode(
    module.eks_cluster.cluster_certificate_authority[0].data
  )
  token = data.aws_eks_cluster_auth.cluster.token
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks_cluster.cluster_name
}

# Create an EKS cluster

module "eks_cluster" {
  source = "C://Users//madus//Desktop//30 Days of Terraform//30-Day-Terraform-challenge-//Day15//eks_cluster_module"

  name = var.cluster_name

  min_size     = 1
  max_size     = 2
  desired_size = 1

  instance_types = ["t3.small"]
}

# Deploy a simple web app into the EKS cluster

module "simple_webapp" {
  source = "C://Users//madus//Desktop//30 Days of Terraform//30-Day-Terraform-challenge-//Day15//k8s_module"

  name = var.app_name

  image          = "training/webapp"
  replicas       = 2
  container_port = 5000

  environment_variables = {
    PROVIDER = "Terraform"
  }

  # Only deploy the app after the cluster has been deployed
  depends_on = [module.eks_cluster]
}

```