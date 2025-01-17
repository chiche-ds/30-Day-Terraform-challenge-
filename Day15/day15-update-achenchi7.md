# Day 15: Working with Multiple Providers - Part 2
## Participant Details

- **Name:** Jully Achenchi
- **Task Completed:** Deploy Docker containers and Kubernetes clusters in AWS using Terraform..
- **Date and Time:** 29/12/2024

```hcl
provider "aws" {
  region = "us-east-1"  # Set my preferred region
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "my-k8s-cluster"
  cluster_version = "1.21" # You can set the desired Kubernetes version
  subnets         = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id

  worker_groups = [
    {
      instance_type = "t3.medium"
      asg_desired_capacity = 2
    }
  ]
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  cidr    = "10.0.0.0/16"
  azs     = ["us-east-1a", "us-east-1b", "us-east-1c"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  default     = "my-k8s-cluster"
}

variable "region" {
  description = "AWS Region"
  default     = "us-east-1"
}

output "cluster_endpoint" {
  description = "Kubernetes Cluster endpoint"
  value       = module.eks.cluster_endpoint
}

output "cluster_name" {
  description = "EKS Cluster Name"
  value       = module.eks.cluster_id
}
```
