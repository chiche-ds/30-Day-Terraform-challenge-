## Day 8: Reusing Infrastructure with Modules

## Participant's Details
**Name:** Major Mbandi

**Task Completed:** Read the chapter on Terraform modules, watched the recommended videos, deployed an EC2 instance using modules, post it on social media(X account)
**Date and Time:** 18/12/24 at 11pm


# Directory Structure
```
/project-root
│
├── main.tf
│
├── modules
│   │
│   ├── ec2
│   │   │
│   │   └── ec2.tf
│   │
│   └── vpc
│      └──vpc.tf
│
├── terraform.tfvars.tf
└── variables.tf

```
# Envronment Structure from deployed using workspaces(dev & prod)
```
/AWS-Account
│
├── dev_environment──dev_vpc
│                   │
│                   └──dev_ec2
│
└──Prod_environment──prod_vpc
                    │
                    └──prod_ec2
```
# Terraform Code

## 1. Creation remote backend
### provider definition
```
  provider "aws" {
    region = "us-east-1"
}
```
### S3 bucket creation

``` resource "aws_s3_bucket" "terraform_state" {
  bucket = "major-s3-state-bucket-day8"
  #Prevent accidental dletion of the bucket
  lifecycle {
    prevent_destroy = true
  }
}
```
### Enable versioning so you can see the full revision history of your state files

``` resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
  depends_on = [aws_s3_bucket.terraform_state]
}
```

### Enable server-side encryption by default

 ``` resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```

### Explicitly block all public access to the S3 bucket
``` resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```
### define DynamoDb for locking
```
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "majorDynamoDb-locks-day8"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}
```
## 2. main.tf
``` terraform {
  required_version = ">= 1.0.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  #remote-back-edn configuration
  backend "s3" {
    bucket         = "major-s3-state-bucket-day8"
    key            = "workspace-default/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "majorDynamoDb-locks-day8"
    encrypt        = true

  }
}

#provider block
provider "aws" {
  region     = var.region
  access_key = var.access_key
  secret_key = var.secret_key
}



module "ec2-deploy" {
  source = "../modules/ec2"
}

module "vpc-deploy" {
  source = "../modules/vpc"
}
```
## 3. modules code

### modules/vpc.tf
``` module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.17.0"  # Or the version you prefer

  name          = "${terraform.workspace}_vpc"
  cidr          = "10.0.0.0/16"
  azs           = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = true

  tags = {
    Terraform   = "true"
    Environment = "lab"
  }
}
```

### modules/ec2.tf
```
resource "aws_instance" "ec2"{
    ami= "ami-0c101f26f147fa7fd"
    instance_type ="t2.micro"


    tags ={
        Name = "${terraform.workspace}_server"
    }
}
```
## conlusion
in this challenge i have created remote backend to be used with my terraform code then created two modules one locally(ec2) and another module that fetch from Terraform registry(vpc) them invoke them to root module(main.tf).
I have also made use of Terraform versioning of vpc module and used workspaces to deploy two separate environment using dev and prod workspaces