# Day 14: Working With Multiple Providers: Part 1

## Participant Details

- **Name:** Eddie Chem
- **Task Completed:** Started Chapter 7 and reviewed video 15, 26 & 27 from the course. Gained an understanding of the underlying components of Terraform Provider blocks
- and the Terraform core.
- **Date and Time:** 12/09/24 10:26 PM

## Terraform Code 
## Working with Multiple providers:
This Terraform block is a provider configuration block that specifies the required Terraform version and providers i.e the `aws` `http`
and `random` providers from the Hashicorp registry, and versions 3.1.0 and 2.1.0.
```hcl
terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
    http = {
      source  = "hashicorp/http"
      version = "2.1.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.1.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "2.1.0"
    }
  }
}
```
## Working with Multiple AWS Regions:

`main.tf`
```hcl
- To specify provider configurations for each region:

 provider "aws" {
  region = "us-east-2"
  alias  = "region_1"
 }
 provider "aws" {
  region = "us-west-1"
  alias  = "region_2"
 }

- To specify providers for each aws_region data source:

data "aws_region" "region_1" {
  provider = aws.region_1
 }
 data "aws_region" "region_2" {
  provider = aws.region_2
 }

```
`output.tf`
```hcl
 output "region_1" {
  value       
= data.aws_region.region_1.name
  description = "The name of the first region"
 }
 output "region_2" {
  value       
= data.aws_region.region_2.name
  description = "The name of the second region"
 }
```
## Architecture 

![Preview](https://drive.google.com/uc?id=1gdq1l8ahyQpZv9DAxLQNf0F6T-kIk6AA)



