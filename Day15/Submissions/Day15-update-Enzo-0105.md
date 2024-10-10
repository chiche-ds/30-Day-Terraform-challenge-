# Day 15: Working with Multiple Providers - Part 2

## Participant Details

- **Name:** Salako Lateef
- **Task Completed:** Working with Multiple Providers - Part 2
- **Date and Time:** 2024-10-03 18:27 PM 

## main.tf that deploys container
```
provider "aws" {
  region = var.region
}

# EKS Cluster module
module "eks" {
  source          = "./modules/eks"
  cluster_name    = var.cluster_name
  region          = var.region
  node_instance_type = var.node_instance_type
  desired_capacity   = var.desired_capacity
  vpc_id          = var.vpc_id
  subnet_ids      = var.subnet_ids
}

# Kubernetes deployment for a Docker container
resource "kubernetes_deployment" "nginx" {
  metadata {
    name      = "nginx-deployment"
    namespace = "default"
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "nginx"
      }
    }

    template {
      metadata {
        labels = {
          app = "nginx"
        }
      }

      spec {
        container {
          image = "nginx:latest"
          name  = "nginx"
          ports {
            container_port = 80
          }
        }
      }
    }
  }
}

# Kubernetes Service to expose the Docker container
resource "kubernetes_service" "nginx_service" {
  metadata {
    name      = "nginx-service"
    namespace = "default"
  }

  spec {
    selector = {
      app = "nginx"
    }

    port {
      port        = 80
      target_port = 80
    }

    type = "LoadBalancer"
  }
}

```
## variables.tf 
```
variable "region" {
  description = "AWS region to deploy the EKS cluster"
  default     = "us-west-2"
}

variable "cluster_name" {
  description = "EKS Cluster name"
  default     = "my-eks-cluster"
}

variable "node_instance_type" {
  description = "EC2 instance type for the EKS nodes"
  default     = "t3.medium"
}

variable "desired_capacity" {
  description = "Desired number of worker nodes"
  default     = 2
}

variable "vpc_id" {
  description = "VPC ID where the EKS cluster will be deployed"
}

variable "subnet_ids" {
  description = "List of subnet IDs for the EKS cluster"
  type        = list(string)
}

```
## modules.tf that create eks cluster
```
module "eks_cluster" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  cluster_version = "1.21"
  subnets         = var.subnet_ids
  vpc_id          = var.vpc_id

  node_groups = {
    eks_nodes = {
      desired_capacity = var.desired_capacity
      instance_type    = var.node_instance_type
      max_capacity     = 3
      min_capacity     = 1
    }
  }
}
```

## variables.tf 
```
variable "cluster_name" {
  description = "Name of the EKS cluster"
}

variable "region" {
  description = "AWS region"
}

variable "node_instance_type" {
  description = "EC2 instance type for worker nodes"
}

variable "desired_capacity" {
  description = "Desired capacity for the node group"
}

variable "vpc_id" {
  description = "VPC ID for the EKS cluster"
}

variable "subnet_ids" {
  description = "List of subnet IDs"
  type        = list(string)
}
```
