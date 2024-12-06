# Day 12: Zero-Downtime Deployment with Terraform

## Participant Details

- **Name:** Eddie Chem
- **Task Completed:** All tasks for Day 12 
- **Date and Time:** 12/2/2024 8:05 PM

## Terraform Code 
The configuration sets up a cluster of web servers using EC2 instances managed by an Auto Scaling Group.
The Auto Scaling Group is set up to perform zero-downtime deployments using instance refresh. This means that 
whenever any parameters in the module are changed, the deployment will be updated without interrupting service. 

This configuration is situated in the directory: `live/prod/services/webserver-cluster-instance-refresh`

`main.tf`
```hcl
terraform {
  required_version = ">= 1.0.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

module "webserver_cluster" {
  source = "../../../../modules/services/webserver-cluster-instance-refresh"

  ami         = "ami-0fb653ca2d3203ac1"

  server_text = var.server_text

  cluster_name           = var.cluster_name
  db_remote_state_bucket = var.db_remote_state_bucket
  db_remote_state_key    = var.db_remote_state_key

  instance_type      = "t2-micro"
  min_size           = 2
  max_size           = 10
  enable_autoscaling = true
}
```
`outputs.tf`
``` hcl
output "alb_dns_name" {
  value       = module.webserver_cluster.alb_dns_name
  description = "The domain name of the load balancer"
}
```
`variables.tf`
``` hcl
variable "db_remote_state_bucket" {
  description = "The name of the S3 bucket used for the database's remote state storage"
  type        = string
}

variable "db_remote_state_key" {
  description = "The name of the key in the S3 bucket used for the database's remote state storage"
  type        = string
}

variable "cluster_name" {
  description = "The name to use to namespace all the resources in the cluster"
  type        = string
  default     = "webservers-prod"
}

variable "server_text" {
  description = "The text for each EC2 instance to display. You can change this text to force a redeploy."
  type        = string
  default     = "Hello, World"
}
```
