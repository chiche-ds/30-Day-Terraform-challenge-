# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** Duncan Gaturu
- **Task Completed:** Completed taks on loops with for_each expressions.
- **Date and Time:** 10/10/2024 10:10PM 

## Terraform Code Snippet showing how to create multiple IAM users with count
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
}

resource "aws_iam_user" "example" {
  count = 3
  name  = "neo.${count.index}"
}
```
