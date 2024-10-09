# Day 20: Workflow for Deploying Application Code

## Participant Details
- **Name:** Njoku Ujunwa Sophia
- **Task Completed:** Workflow for Deploying Application Code
- **Date and Time:** 12/09/2024 08:40 PM

1.  Set Up Terraform Cloud Workspace.
2.  Integrate github with Terraform Cloud.
3.  Add necessary variables in the Terraform Cloud workspace settings like `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
4.  Push changes to GitHub to initiate a Terraform run.

### main.tf
```hcl
terraform { 
  cloud { 
    
    organization = "techynurse" 

    workspaces { 
      name = "ec2-instance-deployment" 
    } 
  } 
}

provider "aws" {
  region = var.region
}

module "ec2_instance" {
  source = "./modules/ec2-instance"
  instance_type  = var.instance_type
  region = var.region
}

variable "region" {
  description = "The AWS region to deploy the instance in"
  default      = "us-east-1"
}

variable "instance_type" {
  description = "The EC2 instance type"
  default     = "t2.micro"
}
```
### ./modules/ec2-instance/modules.tf
```hcl
# ./modules/ec2-instance/main.tf

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

variable "region" {}
variable "instance_type" {}

resource "aws_instance" "this" {
  ami           = data.aws_ami.latest.id 
  instance_type = var.instance_type
  tags = {
    Name = "testing"
  }
}
```


