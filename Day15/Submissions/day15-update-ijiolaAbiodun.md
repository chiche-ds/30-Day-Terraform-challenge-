## Terraform Code 
```hcl
provider "aws" {
    region = "us-east-1"
    alias = "master"
}

provider "aws" {
    region = "us-east-2"
    alias = "slave"

    assume_role {
      role_arn = "arn:aws:iam::ACCOUNT_NUMBER:role/OrganizationAccountAccessRole"
    }
}

data "aws_caller_identity" "master" {
    provider = aws.master
}

data "aws_caller_identity" "child" {
    provider = aws.child
}


## Deploying K8s cluster
### docker/getting-started on k8s

provider "kubernetes" {
  config_path = "~/.kube/config"
  config_context = "docker-desktop"
}

## The webapp exposed on port 80
module "simple_webapp" {
    source = "../../modules/services/k8s-app"
    
    name = "simple-webapp"
    image = "docker"
    replicas = 2
    container_port = 80
}
### Variables
variable "name" {
  description = "The name of the appliance"
  type        = string
}

variable "environment_variables" {
  type        = map(string)
  description = "Environment variables to set for the app"
  default     = {}
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


### Outputs

locals {
    status = kubernetes_service.app.status
}

output "service_endpoint" {
    value = try(
        
"http://${local.status[0]["load_balancer"][0]["ingress"][0]["hostname"]}","(error 
passing hostname from status)"
    )
    description ="The K8S Service endpoint"
}


## main
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


resource "kubernetes_service" "app" {
  metadata {
    name = var.name
  }
  spec {
    type = "LoadBalancer"
    port {
      port = 80
      target_port = var.container_port
      protocol = "TCP"
    }
  selector = local.pod_labels
  }
}

-----------------------------------------------------------
#eks-cluster main.tf

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
    version = "1.30"   # EKS no longer suppports Kubernetes version 1.21 

    vpc_config {
      subnet_ids = data.aws_subnets.default.ids
    }
    # Ensure that IAM Role permissions are created and deleted after the EKS 
Cluster.
    # Otherwise, EKS will not be able to properly delete EKS managed EC2 
infrastructure such as Security groups
    depends_on = [
        aws_iam_role_policy_attachment.AmazonEKSClusterPolicy
    ]

}

# Create IAM role for the node group
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
    # Ensure that IAM Role permissions are created and deleted after the EKS Node 
Group.
    # Otherwise, EKS will not be able to properly delete EC2 instances and ENIs
    depends_on = [
        aws_iam_role_policy_attachment.AmazonEKSWorkerNodePolicy,
        aws_iam_role_policy_attachment.AmazonEC2ContainerRegistryReadOnly,
        aws_iam_role_policy_attachment.AmazonEKS_CNI_Policy,
    ]

}

---------------------------------------------------------------------------
# eks cluster outputs.tf


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
    description = "Certificate Authority of the EKS cluster"
}

---------------------------------------------------------------------------

locals {
    status = kubernetes_service.app.status
}

output "service_endpoint" {
    value = try(
        
"http://${local.status[0]["load_balancer"][0]["ingress"][0]["hostname"]}","(error 
passing hostname from status)"
    )
    description ="The K8S Service endpoint"
}

output "service_endpoint" {
    value = module.simple_webapp.service_endpoint
    description = "The K8S Service endpoint"
}

---------------------------------------------------------------------------------------
## kubernetes-eks main.tf



provider "aws" {
  region = "us-east-2"
}

module "eks_cluster" {
    source = "../../modules/services/eks-cluster"

    name = "example-eks-cluster"
    min_size = 1
    max_size = 2
    desired_size = 1

    # t3.small is the smallest instance type that can be used for worker nodes
    # t2.micre would not work because all the 4 ENIs would be used up and you wont 
be able to deploy your pods
    instance_types = ["t3.small"]
}

## variable.tf


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


```
