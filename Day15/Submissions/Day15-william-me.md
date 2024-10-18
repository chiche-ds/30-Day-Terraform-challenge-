# Day X: Working with Multiple Providers - Part 2

## Participant Details

- **Name:** William Maina
- **Task Completed:** Working with Multiple Providers - Part 2
- **Date and Time:** 18-10-2024

  ## Terraform code
variable.tf
```hcl
variable "name" {
 description = "The name to use for the EKS cluster"
 type = string
}
variable "min_size" {
 description = "Minimum number of nodes to have in the EKS
cluster"
 type = number
}
variable "max_size" {
 description = "Maximum number of nodes to have in the EKS
cluster"
 type = number
}
variable "desired_size" {
 description = "Desired number of nodes to have in the EKS
cluster"
 type = number
}
variable "instance_types" {
 description = "The types of EC2 instances to run in the node
group"
 type = list(string)
}
```
main.tf
```hcl
resource "aws_iam_role" "cluster" {
 name = "${var.name}-cluster-role"
 assume_role_policy =
data.aws_iam_policy_document.cluster_assume_role.json
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
resource "aws_iam_role_policy_attachment"
"AmazonEKSClusterPolicy" {
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
 version = "1.21"
 vpc_config {
 subnet_ids = data.aws_subnets.default.ids
 }
 # Ensure that IAM Role permissions are created before and
deleted after
 # the EKS Cluster. Otherwise, EKS will not be able to properly
delete
 # EKS managed EC2 infrastructure such as Security Groups.
 depends_on = [
 aws_iam_role_policy_attachment.AmazonEKSClusterPolicy
 ]
}
resource "aws_iam_role" "node_group" {
 name = "${var.name}-node-group"
 assume_role_policy =
data.aws_iam_policy_document.node_assume_role.json
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
resource "aws_iam_role_policy_attachment"
"AmazonEKSWorkerNodePolicy" {
 policy_arn =
"arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
 role = aws_iam_role.node_group.name
}
resource "aws_iam_role_policy_attachment"
"AmazonEC2ContainerRegistryReadOnly" {
 policy_arn =
"arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
3
 role = aws_iam_role.node_group.name
}
resource "aws_iam_role_policy_attachment" "AmazonEKS_CNI_Policy"
{
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
 # Ensure that IAM Role permissions are created before and
deleted after
 # the EKS Node Group. Otherwise, EKS will not be able to
properly
 # delete EC2 Instances and Elastic Network Interfaces.
 depends_on = [
 aws_iam_role_policy_attachment.AmazonEKSWorkerNodePolicy,

aws_iam_role_policy_attachment.AmazonEC2ContainerRegistryReadOnly
,
 aws_iam_role_policy_attachment.AmazonEKS_CNI_Policy,
 ]
}

output.tf
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
