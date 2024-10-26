# Day 22: Putting It All Together - Wrapping Up the Book and Celebrating Success! 
## Participant Details

- **Name:** Akintola AbdulAzeez
- **Task Completed:** Putting It All Together - Wrapping Up the Book and Celebrating Success! 
- **Date and Time:** 12/09/2024 11:21 PM



### terraform/modules/ec2-instance/main.tf
```
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
### main.tf
```
terraform { 
  cloud { 
    
    organization = "hayzedak" 

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

### terraform-aws-ec2-instance/.github/workflows/main.yml
```
name: Deploy Infrastructure

on:
  push:
    branches:
      - main

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.3.0

      - name: Print Environment Variables
        run: |
          echo "TF_TOKEN_APP_TERRAFORM_IO: $TF_TOKEN_APP_TERRAFORM_IO"

      - name: Terraform Init
        run: terraform init
        env:
          TF_TOKEN_app_terraform_io: ${{ secrets.TF_TOKEN_APP_TERRAFORM_IO }}

      - name: Terraform Plan
        run: terraform plan
        env:
          TF_TOKEN_app_terraform_io: ${{ secrets.TF_TOKEN_APP_TERRAFORM_IO }}

      - name: Terraform Apply
        run: terraform apply -auto-approve
        env:
          TF_TOKEN_app_terraform_io: ${{ secrets.TF_TOKEN_APP_TERRAFORM_IO }}

      - name: Terraform Destroy
        run: terraform destroy -auto-approve
        env:
          TF_TOKEN_app_terraform_io: ${{ secrets.TF_TOKEN_APP_TERRAFORM_IO }}
```

### restrict_instance_type.sentinel
```
import "tfplan"

resource_tags = tfplan.resource_changes["aws_instance.this"].after.tags

main = rule {
  resource_tags["Name"] == "testing"
}
```
