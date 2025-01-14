# Day 13: Managing Sensitive Data in Terraform

 day24-final-prep
## Participant Details


- **Name:** Jully Achenchi
- **Task Completed:** Understood Terraform Managing Sensitive Data in Terraform
- **Date and Time:** 27/12/2024

## **Do not store secrets in plain text.**

1.Providers authentication
```
#Human users on their computers
--> use environment variables ()
 $ export AWS_ACCESS_KEY_ID = (YOUR_ACCESS_KEY_ID)
 $ export AWS_SECRET_ACCESS_KEY=(YOUR_SECRET_ACCESS_KEY)
###ensures code is stored in memory and not disk.
```

2. For Resources and Data Sources:
   
   2.1 mark the sensitive = true
   
```hcl
variable "db_username" {
    description = "The username for the database"
    type = string
    sensitive = true
}

variable "db_password" {
    description = "The password for the database"
    type = string
    sensitive = true
}

#these variables do not have a default

resource "aws_db_instance" "db_example" {
    identifier_prefix = "terraform-up-and-running"
    engine = "mysql"
    allocated_storage = 10
    instance_class = "db.t2.micro"
    skip_final_snapshot = true
    db_name = "example_database"

    username = var.db_username
    password = var.db_password
  #pass those secrets into Terraform via environment variables.
  #don't pass username & password as they are sensitive
}
```
 2.2.Secret Stores (store your database credentials in AWS Secrets Manager on the AWS Web Console)
 
 ```HCL
#AWS Secrets Manager
#store your database credentials in AWS Secrets Manager on AWS Web Console


data "aws_secretsmanager_secret_version" "creds"{
    secret_id = "db-creds"
}

#use the jsondecode function to parse the
#JSON into the local variable db_creds
locals {
    db_creds = jsondecode(
        data.aws_secretsmanager_secret_version.secret_string
    )
}

#read db credentials from db_creds
resource "aws_db_instance" "example" {
    identifier_prefix = "terraform-up-and-running"
    engine = "mysql"
    allocated_storage = 10
    instance_class = "db.t2.micro"
    skip_final_snapshot = true
    db_name = var.db_name

    #pass secrets to resource
    username = local.db_creds.username
    password = local.db_creds.password
}
```
