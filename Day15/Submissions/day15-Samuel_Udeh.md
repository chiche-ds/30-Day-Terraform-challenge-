Day 15: Working with Multiple Providers - Part 2
Name: Udeh Samuel Chibuike
Task Completed: Deploy Docker containers in AWS using Elastic Kubernetes Service (EKS) managed by Terraform.
Date and Time: 4/1/2025 10:25pm

# For eks_cluster_module

# main.tf

# Create an IAM role for the control plane
resource "aws_iam_role" "cluster" {
 name = "${var.name}-cluster-role"
 assume_role_policy = data.aws_iam_policy_document.cluster_assume_role.json
}
# Allow EKS to assume the IAM role
data "aws_iam_policy_document" "cluster_assume_role" {
 statement {
 effect = "Allow"
 actions = ["sts:AssumeRole"]
 principals {
 type = "Service"
 identifiers = ["eks.amazonaws.com"]
 }
 }
}
# Attach the permissions the IAM role needs
resource "aws_iam_role_policy_attachment" "AmazonEKSClusterPolicy" {
 policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
 role = aws_iam_role.cluster.name
}
# Since this code is only for learning, use the Default VPC and subnets.
# For real-world use cases, you should use a custom VPC and private subnets.
data "aws_vpc" "default" {
 default = true
}
data "aws_subnets" "default" {
 filter {
 name = "vpc-id"
 values = [data.aws_vpc.default.id]
 }
}
resource "aws_eks_cluster" "cluster" {
 name = var.name
 role_arn = aws_iam_role.cluster.arn
 version = "1.26"
 vpc_config {
 subnet_ids = data.aws_subnets.default.ids
 }
 # Ensure that IAM Role permissions are created before and deleted after
 # the EKS Cluster. Otherwise, EKS will not be able to properly delete
 # EKS managed EC2 infrastructure such as Security Groups.
 depends_on = [
 aws_iam_role_policy_attachment.AmazonEKSClusterPolicy
 ]
}
# Create an IAM role for the node group
resource "aws_iam_role" "node_group" {
 name = "${var.name}-node-group"
 assume_role_policy = data.aws_iam_policy_document.node_assume_role.json
}
# Allow EC2 instances to assume the IAM role
data "aws_iam_policy_document" "node_assume_role" {
 statement {
 effect = "Allow"
 actions = ["sts:AssumeRole"]
principals {
 type = "Service"
 identifiers = ["ec2.amazonaws.com"]
 }
 }
}
# Attach the permissions the node group needs
resource "aws_iam_role_policy_attachment" "AmazonEKSWorkerNodePolicy" {
 policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
 role = aws_iam_role.node_group.name
}
resource "aws_iam_role_policy_attachment" "AmazonEC2ContainerRegistryReadOnly" {
 policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
 role = aws_iam_role.node_group.name
}
resource "aws_iam_role_policy_attachment" "AmazonEKS_CNI_Policy" {
 policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
 role = aws_iam_role.node_group.name
}
resource "aws_eks_node_group" "nodes" {
 cluster_name = aws_eks_cluster.cluster.name
 node_group_name = var.name
 node_role_arn = aws_iam_role.node_group.arn
 subnet_ids = data.aws_subnets.default.ids
 instance_types = var.instance_types
 scaling_config {
 min_size = var.min_size
 max_size = var.max_size
 desired_size = var.desired_size
 }
 # Ensure that IAM Role permissions are created before and deleted after
 # the EKS Node Group. Otherwise, EKS will not be able to properly
 # delete EC2 Instances and Elastic Network Interfaces.
 depends_on = [
 aws_iam_role_policy_attachment.AmazonEKSWorkerNodePolicy,
 aws_iam_role_policy_attachment.AmazonEC2ContainerRegistryReadOnly,
 aws_iam_role_policy_attachment.AmazonEKS_CNI_Policy,
 ]
}

# outputs.tf

output "cluster_name" {
 value = aws_eks_cluster.cluster.name
 description = "Name of the EKS cluster"
}
output "cluster_arn" {
 value = aws_eks_cluster.cluster.arn
 description = "ARN of the EKS cluster"
}
output "cluster_endpoint" {
 value = aws_eks_cluster.cluster.endpoint
 description = "Endpoint of the EKS cluster"
}
output "cluster_certificate_authority" {
 value = aws_eks_cluster.cluster.certificate_authority
 description = "Certificate authority of the EKS cluster"
}

# variable.tf

variable "name" {
 description = "The name to use for the EKS cluster"
 type = string
}
variable "min_size" {
 description = "Minimum number of nodes to have in the EKS cluster"
 type = number
}
variable "max_size" {
 description = "Maximum number of nodes to have in the EKS cluster"
type = number
}
variable "desired_size" {
 description = "Desired number of nodes to have in the EKS cluster"
 type = number
}
variable "instance_types" {
 description = "The types of EC2 instances to run in the node group"
 type = list(string)
}

# K8s_app

# main.tf

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
  source = "../eks_cluster_module"

  name = var.cluster_name

  min_size     = 1
  max_size     = 2
  desired_size = 1

  instance_types = ["t3.small"]
}

# Deploy a simple web app into the EKS cluster

module "simple_webapp" {
  source = "../k8s_app_module"

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

# outputs.tf

output "cluster_arn" {
  value       = module.eks_cluster.cluster_arn
  description = "ARN of the EKS cluster"
}

output "cluster_endpoint" {
  value       = module.eks_cluster.cluster_endpoint
  description = "Endpoint of the EKS cluster"
}

output "service_endpoint" {
  value       = module.simple_webapp.service_endpoint
  description = "The K8S Service endpoint"
}

# variable.tf

variable "cluster_name" {
  description = "The name to use for the EKS cluster and all its associated resources"
  type        = string
  default     = "kubernetes-example"
}

variable "app_name" {
  description = "The name to use for the app deployed into the EKS cluster"
  type        = string
  default     = "simple-webapp"
}

# K8s_app_m0dule

# main.tf

terraform {
  required_version = ">= 1.0.0, < 2.0.0"

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

locals {
  pod_labels = {
    app = var.name
  }
}

# Create a simple Kubernetes Deployment to run an app
resource "kubernetes_deployment" "app" {
  metadata {
    name = var.name
  }

  spec {
    replicas = var.replicas

    template {
      metadata {
        labels = local.pod_labels
      }

      spec {
        container {
          name  = var.name
          image = var.image

          port {
            container_port = var.container_port
          }

          dynamic "env" {
            for_each = var.environment_variables
            content {
              name  = env.key
              value = env.value
            }
          }
        }
      }
    }

    selector {
      match_labels = local.pod_labels
    }
  }
}

# Create a simple Kubernetes Service to spin up a load balancer in front
# of the app in the Kubernetes Deployment.
resource "kubernetes_service" "app" {
  metadata {
    name = var.name
  }

  spec {
    type = "LoadBalancer"
    port {
      port        = 80
      target_port = var.container_port
      protocol    = "TCP"
    }
    selector = local.pod_labels
  }
}

# outputs.tf

output "service_status" {
  value       = kubernetes_service.app.status
  description = "The K8S Service status"
}

locals {
  status = kubernetes_service.app.status
}
#Exposing the service enpoint
output "service_endpoint" {
  value = try(
    "http://${local.status[0]["load_balancer"][0]["ingress"][0]["hostname"]}",
    "(error parsing hostname from status)"
  )
  description = "The K8S Service endpoint"
}

# variables.tf

variable "name" {
  description = "The name to use for all resources created by this module"
  type        = string
}

variable "image" {
  description = "The Docker image to run"
  type        = string
}

variable "container_port" {
  description = "The port the Docker image listens on"
  type        = number
}

variable "replicas" {
  description = "How many replicas to run"
  type        = number
}


variable "environment_variables" {
  description = "Environment variables to set for the app"
  type        = map(string)
  default     = {}
}


