# Day 15: Working with Multiple Providers - Part 2

## Participant Details

- **Name:** Utibe Okon (yutee)
- **Task Completed:** Working with multiple different providers. Integrating kubernetes providers with aws in terraform.
- **Date and Time:** Mon 14th October, 2024 | 2:49 PM GMT+1

### Overview

## Terraform Code 
```hcl
terraform {
    required_version = ">= 1.0.0, < 2.0.0"
    required_providers {

        aws = {
            region = us-east1
        }

        kubernetes = {
        source = "hashicorp/kubernetes"
        version = "~> 2.0"
        }
    }
}

```