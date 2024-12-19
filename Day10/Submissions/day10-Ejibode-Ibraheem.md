# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** Ejibode Ibraheem A
- **Task Completed:** Use conditionals to deploy resources only when certain conditions are met
- **Date and Time:** 14/12/2024 12:45 PM

## Implementing Conditional Logic using `count` to Deploy Multiple Instances
### modules.tf

```hcl
provider "aws" {
  region = var.region
}

data "aws_ami" "latest" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["amazon"]
}

resource "aws_instance" "this" {
  count         = var.create_ec2_instance ? var.instance_count : 0
  ami           = data.aws_ami.latest.id
  instance_type = var.instance_type
  tags = {
    Name = "testing-${count.index + 1}"
  }
}

variable "region" {}
variable "instance_count" {}
variable "create_ec2_instance" {}
variable "instance_type" {}
```

### main.tf

```hcl
module "ec2_instance" {
  source = "./terraform-modules/ec2-instance"
  instance_count      = var.instance_count
  create_ec2_instance = var.create_ec2_instance
  region              = var.region
  instance_type       = var.instance_type
}

variable "region" {
  description = "The AWS region to deploy the instance in"
  default     = "us-east-2"
}

variable "instance_count" {
  description = "Number of EC2 instances to deploy"
  default     = 2
}

variable "instance_type" {
  description = "The EC2 instance type"
  default     = "t2.micro"
}

variable "create_ec2_instance" {
  description = "Whether to create EC2 instances"
  type        = bool
  default     = true
}
```


## Using for_each to Iterate Over Maps or Lists
### modules.tf

```hcl
variable "region" {
  description = "The AWS region to deploy the instances in"
  default     = "us-east-1"
}

variable "instances" {
  description = "Map of instances to create"
  type = map(object({
    instance_type = string
    ami           = string
  }))
  default = {
    "web-server-1" = {
      instance_type = "t2.micro"
      ami           = "ami-0e86e20dae9224db8"  # Replace with a valid AMI ID
    }
    "web-server-2" = {
      instance_type = "t2.small"
      ami           = "ami-0e86e20dae9224db8"  # Replace with a valid AMI ID
    }
  }
}

module "ec2_instance" {
  source    = "./terraform-modules/ec2-instance"
  instances = var.instances
}
```
### main.tf
```hcl
variable "instances" {
  description = "Map of instances to create"
  type        = map(object({
    instance_type = string
    ami           = string
  }))
  default = {}
}


resource "aws_instance" "this" {
  for_each      = var.instances
  ami           = each.value.ami
  instance_type = each.value.instance_type

  tags = {
    Name = each.key
  }
}
```
