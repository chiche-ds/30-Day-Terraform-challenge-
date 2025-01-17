# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** Major Mbandi
- **Task Completed:** Terraform Loops and Conditionals
- **Date and Time:** 20/12/2024 10:49pm

# Terraform code
```
#provider details

terraform {
  required_version = ">= 1.0.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Input Variables
variable "deploy_instances" {
  description = "Flag to control whether to deploy EC2 instances"
  type        = bool
  default     = true
}

variable "instance_count" {
  description = "Number of instances to deploy"
  type        = number
  default     = 3
}

# Data source to get the available Availability Zones
data "aws_availability_zones" "available" {}

# EC2 Instance resource
resource "aws_instance" "myservers" {
  ami           = "ami-0c101f26f147fa7fd"
  instance_type = "t2.micro"
  count         = var.deploy_instances ? var.instance_count : 0

  # Distribute instances across availability zones
  availability_zone = data.aws_availability_zones.available.names[count.index % length(data.aws_availability_zones.available.names)]

  tags = {
    Name = "MejjaServer_${count.index}"
  }
}

```