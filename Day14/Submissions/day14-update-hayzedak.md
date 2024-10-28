# Day 14: Managing Sensitive Data in Terraform


## Participant Details

- **Name:** Akintola AbdulAzeez 
- **Task Completed:** Terraform configurations using multiple copies of the same provider and Experiment with provider aliases and versions.
- **Date and Time:** 16/10/2024 03:56 PM 

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  alias  = "us_east"
  region = "us-east-1"
  version = "~> 3.0"
}

provider "aws" {
  alias  = "us_west"
  region = "us-west-2"
  version = "~> 3.0"
}

provider "aws" {
  alias  = "account_1"
  region = "us-east-1"
  profile = "account1_profile"
}

provider "aws" {
  alias  = "account_2"
  region = "us-west-2"
  profile = "account2_profile"
}

resource "aws_instance" "us_east_instance" {
  provider      = aws.us_east
  ami           = "ami-0e86e20dae9224db8"
  instance_type = "t2.micro"
  tags = {
    Name = "us-east-instance"
  }
}

resource "aws_instance" "us_west_instance" {
  provider      = aws.us_west
  ami           = "ami-0e86e20dae9224db8"
  instance_type = "t2.micro"
  tags = {
    Name = "us-west-instance"
  }
}

resource "aws_instance" "account_1_instance" {
  provider      = aws.account_1
  ami           = "ami-0e86e20dae9224db8"
  instance_type = "t2.micro"
  tags = {
    Name = "account-1-instance"
  }
}

resource "aws_instance" "account_2_instance" {
  provider      = aws.account_2
  ami           = "ami-0e86e20dae9224db8"
  instance_type = "t2.micro"
  tags = {
    Name = "account-2-instance"
  }
}
```
