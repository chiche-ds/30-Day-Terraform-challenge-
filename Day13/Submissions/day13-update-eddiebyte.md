# Day 13: Managing Sensitive Data in Terraform

## Participant Details

- **Name:** Eddie Chem
- **Task Completed:** All tasks for Day 13 
- **Date and Time:** 12/8/2024 10:40 PM

## Terraform Code 
This Terraform code manages the provisioning of an AWS RDS (Relational Database Service) 
instance securely by using AWS Secrets Manager to handle sensitive information like database credentials, and AWS Vault to 
handle authentication and provide access to the AWS Secrets Manager.

- After downloading and installing AWS Vault run the command: `aws-vault add my-profile` to enter AWS access key and secret key.
- Use AWS Vault to Authenticate and Run Terraform with `aws-vault exec my-profile -- terraform apply` (Replace `my-profile` with
the name of the profile you set up in AWS Vault.)

AWS Vault automatically exports temporary AWS credentials as environment variables `(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN)`, and then
uses these credentials to authenticate with AWS and fetch the secret `(db-creds)` from Secrets Manager.


`main.tf`
```hcl
terraform {
  required_version = ">= 1.0.0, < 2.0.0"

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

data "aws_secretsmanager_secret_version" "creds" {
  secret_id = "db-creds"
}

locals {
  db_creds = jsondecode(
    data.aws_secretsmanager_secret_version.creds.secret_string
  )
}

resource "aws_db_instance" "my_app_db" {
  identifier_prefix   = "my_app"
  engine              = "mysql"
  allocated_storage   = 10
  instance_class      = "db.t2.micro"
  skip_final_snapshot = true
  db_name             = var.db_name

  # Pass the secrets to the resource
  username = local.db_creds.username
  password = local.db_creds.password
}
```

