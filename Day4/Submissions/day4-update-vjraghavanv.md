# Day 4: Mastering Basic Infrastructure with Terraform

## Participant Details

- **Name:** Vijayaraghavan Vashudevan
- **Task Completed:** Learnt - How to use input and local variables in Terraform for more flexible and reusable configurations, and hands-on of Deployment of Highly Available Web App on AWS using Terraform.
- **Date and Time:** 22-08-2024 at 23:40 pm IST

### main.tf
```bash
# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Launch Template
resource "aws_launch_template" "terraform_temp" {
  name_prefix   = "Terraform_Challenge"
  image_id      = "ami-02e136e904f3da870"
  instance_type = "t2.micro"
}

# Auto Scaling Group
resource "aws_autoscaling_group" "terraform_group" {
  name               = "Terraform-ASG1"
  availability_zones = ["us-east-1a", "us-east-1b"]
  desired_capacity   = 2
  max_size           = 10
  min_size           = 2
  launch_template {
    id      = aws_launch_template.terraform_temp.id
    version = "$Latest"
  }
}
```
### terraform.tf
```bash
terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.1.0"
    }
  }
}
```
### output.tf
```bash
output "launchtemplate" {
  value = aws_launch_template.terraform_temp.arn
}
output "autoscaling_group" {
  value = aws_autoscaling_group.terraform_group.arn
}
```
### Architecture/Flow Diagram of Web-App Server using Terraform

![Architecture/Flow Diagram of High Available Web-App server using Terraform](ASG_vjraghavanv.gif)
