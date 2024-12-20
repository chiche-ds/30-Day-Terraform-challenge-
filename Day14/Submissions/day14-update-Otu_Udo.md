# Day 14: Working with Multiple Providers - Part 1

## Participant Details

- **Name:** Otu Michael Udo
- **Task Completed:** Deployed two ec2 instances to two different regions on aws.
- **Date and Time:** 20th December, 2024 | 07:14 PM

Using different regions can be acheived with aliases. An alias is a custom name for the provider, which you can explicitly pass to individual resources, data sources, and modules to get them to use the configuration in that particular provider. To tell those aws_region data sources to use a specific provider, you set the provider parameter as follows:

As an extra tip, I also learnt that ading required providers at the module level is important when trying to deploy to multiple regions.

## Terraform Code 
```hcl
# main.tf
terraform {
 required_providers {
    aws = {
 source = "hashicorp/aws"
 version = "~> 4.0"
 }
 }
}
provider "aws" {
 region = "us-east-1"
 alias = "region_1"
}
provider "aws" {
 region = "us-west-1"
 alias = "region_2"
}
data "aws_region" "region_1" {
 provider = aws.region_1
}
data "aws_region" "region_2" {
 provider = aws.region_2
}
output "region_1" {
 value = data.aws_region.region_1.name
 description = "The name of the first region"
}
output "region_2" {
 value = data.aws_region.region_2.name
 description = "The name of the second region"
}
# Helps find AMI IDs for you automatically instead of searching manually since AMI are unique to each region .
data "aws_ami" "ubuntu_region_1" {
 provider = aws.region_1
 most_recent = true
 owners = ["099720109477"] # AWS account ID for Canonical, the official provider of Ubuntu images
 filter {
 name = "name"
 values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
 }
}
data "aws_ami" "ubuntu_region_2" {
 provider = aws.region_2
 most_recent = true
 owners = ["099720109477"] # AWS account ID for Canonical, the official provider of Ubuntu images
 filter {
 name = "name"
 values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
 }
}
resource "aws_instance" "region_1" {
 provider = aws.region_1
 ami = data.aws_ami.ubuntu_region_1.id
 instance_type = "t2.micro"
}
resource "aws_instance" "region_2" {
 provider = aws.region_2
 ami = data.aws_ami.ubuntu_region_2.id
 instance_type = "t2.micro"
}
output "instance_region_1_az" {
 value = aws_instance.region_1.availability_zone
 description = "The AZ where the instance in the first region deployed"
}
output "instance_region_2_az" {
 value = aws_instance.region_2.availability_zone
 description = "The AZ where the instance in the second region deployed"
}
```