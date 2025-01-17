# Day 15: Working with Multiple Providers - Part 2

## Participant Details

- **Name:** Dwayne Chima
- **Task Completed:** Deploy Docker containers and Kubernetes clusters in AWS using Terraform
- **Date and Time:** 14th Dec 2024 3:40am

## Terraform Code

### **main.tf**
```hcl
module "policies" {
  source = "./modules/policies"
}

module "networks" {
  source = "./modules/network"
  dns_hostnames = "true"
  dns_support = "true"
  tags = {
    name = "eks_cluster"
  }
  region = var.region
}

module "cluster" {
  source = "./modules/cluster"
  tags = {
    name = "eks_cluster"
  }
  public_subnets = module.networks.public_subnets
  private_subnets =module.networks.private_subnets
  eks_version = "1.31"
  ami_type = "AL2_x86_64"
  capacity_type = "ON_DEMAND"
  roles       = module.policies.roles
  attachments = module.policies.attachments
}
```

***


### **modules/iam.tf**
```hcl
# IAM Role for EKS Cluster to assume
resource "aws_iam_role" "cluster_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com" 
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# IAM Role for Worker Nodes to assume
resource "aws_iam_role" "worker_node_role" {
  name = "worker_node_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# IAM Policy for EKS Autoscaling
resource "aws_iam_policy" "eks_autoscaling_policy" {
  name   = "EksAutoScalingPolicy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect: "Allow",
        Action: [
          # Permissions to describe autoscaling resources
          "autoscaling:DescribeAutoScalingGroups",
          "autoscaling:DescribeAutoScalingInstances",
          "autoscaling:DescribeLaunchConfigurations",
          "autoscaling:DescribeScalingActivities",
          "autoscaling:DescribeTags",
          "ec2:DescribeInstanceTypes",
          "ec2:DescribeLaunchTemplateVersions"
        ],
        Resource: ["*"]
      },
      {
        Effect: "Allow",
        Action: [
          # Permissions to modify autoscaling settings and describe EKS nodegroups
          "autoscaling:SetDesiredCapacity",
          "autoscaling:TerminateInstanceInAutoScalingGroup",
          "ec2:DescribeImages",
          "ec2:GetInstanceTypesFromInstanceRequirements",
          "eks:DescribeNodegroup"
        ],
        Resource: ["*"]
      }
    ]
  })
}



# Attach policies to the cluster and Worker Node roles
resource "aws_iam_role_policy_attachment" "cluster_role_policy_attach" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.cluster_role.name
}

resource "aws_iam_role_policy_attachment" "worker_node_role_policy_attach" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.worker_node_role.name
}

resource "aws_iam_role_policy_attachment" "CNI_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.worker_node_role.name
}

resource "aws_iam_role_policy_attachment" "EC2CR_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.worker_node_role.name
}

resource "aws_iam_role_policy_attachment" "EKSAutoScaling_policy_attachment" {
  policy_arn = aws_iam_policy.eks_autoscaling_policy.arn
  role       = aws_iam_role.worker_node_role.name
}
```

***

### **modules/cluster.tf**
```hcl
# EKS Cluster Creation
resource "aws_eks_cluster" "eks_cluster" {
  name     = "my_eks_cluster"  
  role_arn = var.roles.cluster_role  
  version  = var.eks_version 

  # VPC configuration for the EKS cluster
  vpc_config {
    subnet_ids = concat(
      values(var.private_subnets)[*].id, 
      values(var.public_subnets)[*].id   
    )
  }

  depends_on = [var.attachments]  # Ensures that IAM roles are created before the EKS cluster
  tags = var.tags 
}

# EKS Node Group Creation
resource "aws_eks_node_group" "Node_group" {
  cluster_name    = aws_eks_cluster.eks_cluster.name  
  node_group_name = "eks_node_group"  
  node_role_arn   = var.roles.worker_node_role
  subnet_ids      = values(var.private_subnets)[*].id 

  # Scaling configuration for the node group
  scaling_config {
    desired_size = var.desired_size 
    max_size     = var.max_size      
    min_size     = var.min_size      
  }

  # Update configuration for the node group
  update_config {
    max_unavailable = var.max_unavailable  # Max unavailable nodes during updates
  }

  ami_type        = var.ami_type  
  instance_types  = var.instance_type  
  capacity_type   = var.capacity_type  

  depends_on = [var.attachments] 
  tags = var.tags 
}

provider "kubernetes" {
  host = aws_eks_cluster.eks_cluster.endpoint
  token = aws_eks_cluster_auth.eks_cluster_auth.token
  cluster_ca_certificate = base64decode(aws_eks_cluster.eks_cluster.certificate_authority[0].data)
}

resource "kubernetes_deployment" "app_deployment" {
  metadata {
    name = var.name
  }

  spec {
    replicas = var.replicas
    selector {
      match_labels = local.pod_labels
    }

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
  }
}


resource "kubernetes_service" "app_service" {
  metadata {
    name = "${var.name}-service"
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
```
