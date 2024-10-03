# Day 13: Managing Sensitive Data in Terraform

## Participant Details

- **Name:** Salako Lateef 
- **Task Completed:** Managing Sensitive Data in Terraform
- **Date and Time:** 2024-10-03 15:54 AM GMT

main.tf
```
provider "aws" {
  region = "us-east-1"
}
data "aws_secretsmanager_secret_version" "big-name" {
  secret_id = "bigname"
}

output "test" {
  value = data.aws_secretsmanager_secret_version.big-name
  sensitive = true
}
```
