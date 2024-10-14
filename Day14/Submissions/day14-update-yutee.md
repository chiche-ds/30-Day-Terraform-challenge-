# Day 14: Working with Multiple Providers - Part 1

## Participant Details

- **Name:** Utibe Okon (yutee)
- **Task Completed:** Deployed two ec2 instances to two different regions on aws.
- **Date and Time:** Mon 14th October, 2024 | 9:23 AM GMT+1

Using different regions can be acheived with aliases. An alias is a custom name for the provider, which you can explicitly pass to individual resources, data sources, and modules to get them to use the configuration in that particular provider. To tell those aws_region data sources to use a specific provider, you set the provider parameter as follows:

As an extra tip, I also learnt that ading required providers at the module level is important when trying to deploy to multiple regions.

## Terraform Code 
```hcl
# provider.tf
provider "aws" {
    region = "us-east-2"
    alias = "region_1"
}

provider "aws" {
    region = "us-west-1"
    alias = "region_2"
}

resource "aws_instance" "server1" {
    provider = aws.region_1
    ami = "ami-0fb653ca2d3203ac1"
    instance_type = "t2.micro"
}

resource "aws_instance" "server2" {
    provider = aws.region_2
    ami = "ami-01f87c43e618bf8f0"
    instance_type = "t2.micro"
}
```