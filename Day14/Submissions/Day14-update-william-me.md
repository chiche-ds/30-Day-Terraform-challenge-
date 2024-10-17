# Day 14: Working with Multiple Providers-Part 1

## Participant Details

- **Name:** William Maina
- **Task Completed:** Deploying resources over multiple regions
- **Date and Time:** 21:00

## Terraform Code for deploying two EC2 instances across 2 regions
Main.tf
```hcl
# If you want control over how terraform installs providers
terraform {
 required_providers {
 aws = {
 source = "hashicorp/aws"
 version = "~> 4.0"
 }
}

}
provider "aws" {
  alias  = "region_1"
  region = "us-east-1"
}

provider "aws" {
  alias  = "region_2"
  region = "us-west-2"
}

# Resource for EC2 instance in us-east-1
resource "aws_instance" "east_instance" {
  provider = aws.region_1
  ami      = "ami-0c55b159cbfafe1f0"  # Replace with your desired AMI ID
  instance_type = "t2.micro"

  tags = {
    Name = "East-Instance"
  }
}

# Resource for EC2 instance in us-west-2
resource "aws_instance" "west_instance" {
  provider = aws.region_2
  ami      = "ami-0c55b159cbfafe1f0"  # Replace with your desired AMI ID
  instance_type = "t2.micro"

  tags = {
    Name = "West-Instance"
  }
}

```
Output.tf
```hcl
output "east_instance_public_ip" {
  description = "The public IP of the EC2 instance in us-east-1"
  value       = aws_instance.east_instance.public_ip
}

output "west_instance_public_ip" {
  description = "The public IP of the EC2 instance in us-west-2"
  value       = aws_instance.west_instance.public_ip
}

```
