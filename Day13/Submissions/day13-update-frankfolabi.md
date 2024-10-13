# Day 13: Managing Sensitive Data in Terraform 

## Participant Details

- **Name:** Franklin Afolabi
- **Task Completed:** Worked on the best way to manage secrets Terraform to avoid exposing secrets in statefiles and configuration files.
- **Date and Time:** September 21 0830

## Terraform Code using AWS secrets manager
```hcl

data "aws_secretsmanager_secret_version" "creds" {
  secret_id = "db-creds"
}

locals {
  db-creds = jsonencode(
    data.aws_secretsmanager_secret_version.creds.secret_string
  )
}

resource "aws_db_instance" "example" {
    identifier_prefix ="terraform-up-and-running"
    engine = "mysql"
    allocated_storage = 10
    instance_class = "db.t3.micro"
    skip_final_snapshot = true
    db_name = "example-database"

    username = local.db-creds.username
    password = local.db-creds.password
}

```
## Architecture 

[Name](link to image in S3 bucket)
