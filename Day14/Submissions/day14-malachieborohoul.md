# Day 14: Working with Multiple Providers - Part 1

## Participant Details

- **Name:** BOROHOUL Soguelni Malachie
- **Task Completed:** I started working with multiple providers by deploying EC2 instances in 2 different AWS regions with the use of aliases. I also understood the benifits of locking provider version.
- **Date and Time:** 9/03/2024 10:20 PM 

## Terraform Code 
Deployed 2 EC2 instances each in different region using aliases

```hcl

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

data "aws_region" "region_1" {
  provider = aws.region_1
}

data "aws_region" "region_2" {
  provider = aws.region_2
}

provider "aws" {
  region = "us-east-2"
  alias  = "region_1"
}

provider "aws" {
  region = "us-west-1"
  alias  = "region_2"
}


output "region_1" {
  value       = data.aws_region.region_1.name
  description = "The name of the first region"
}

output "region_2" {
  value       = data.aws_region.region_2.name
  description = "The name of the second region"
}

resource "aws_instance" "region_1" {
  provider = aws.region_1
  # Note different AMI IDs!!
  ami           = data.aws_ami.ubuntu_region_1.id
  instance_type = "t2.micro"
}

resource "aws_instance" "region_2" {
  provider = aws.region_2
  # Note different AMI IDs!!
  ami           = data.aws_ami.ubuntu_region_2.id
  instance_type = "t2.micro"
}


data "aws_ami" "ubuntu_region_1" {
  provider = aws.region_1

  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

data "aws_ami" "ubuntu_region_2" {
  provider = aws.region_2

  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

```
## Architecture 
[The interaction between the Terraform core, providers, and the outside world.](https://asset.cloudinary.com/dshli1qgh/c48dd137540197acb52c66f558883fee)

