# Day 14: Working with Multiple Providers - Part 1

## Participant Details

- **Name:** Salako Lateef
- **Task Completed:** Multiple provider configuration
- **Date and Time:** 2024-10-03 16:00 PM 

## main.tf
```
provider "aws" {
  alias = "east"
  region = "us-east-1"
}

provider "aws" {
  alias = "east2"
  region = "us-east-2"
}
provider "aws" {
  alias = "west"
  region = "us-west-1"
}

```
