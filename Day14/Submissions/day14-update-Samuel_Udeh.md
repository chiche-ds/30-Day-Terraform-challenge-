Day 14: Working with Multiple Providers - Part 1
Name: Udeh Samuel Chibuike
Task Completed: Set up Terraform configurations that use multiple copies of the same provider, such as deploying resources in multiple AWS regions or accounts
Date and Time: 3/1/2025 8:25pm


provider "aws" {
 region = "us-east-2"
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