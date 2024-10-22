# Day 14: Working with Multiple Providers - Part 1

## Participant Details

- **Name:** **Ajibola Mubarak**
- **Task Completed:**Working with Multiple Providers
- **Date and Time:** 10/22/2024 03:58 PM 

## Terraform Code 
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
  alias  = "region_1"
}
provider "aws" {
  region = "us-west-1"
  alias  = "region_2"
}

data "aws_region" "region_1" {
  provider = aws.region_1
}
data "aws_region" "region_2" {
  provider = aws.region_2
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
  ami           = "ami-0ea3c35c5c3284d82"
  instance_type = "t2.micro"
 } 
resource "aws_instance" "region_2" {
  provider = aws.region_2 
  # Note different AMI IDs!!
  ami           = "ami-0da424eb883458071"
  instance_type = "t2.micro"
 }


output "instance_region_1_az" {
  value       = aws_instance.region_1.availability_zone
  description = "The AZ where the instance in the first region deployed"
}
output "instance_region_2_az" {
  value       = aws_instance.region_2.availability_zone
  description = "The AZ where the instance in the second region deployed"
}


```
## links

[Day14-blog](https://medium.com/@spikes2023/working-with-multiple-providers-part-1-f9b0c96782a3)