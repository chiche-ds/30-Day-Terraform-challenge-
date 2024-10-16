# Day 14: Working with Multiple Providers - Part 1

## Participant Details

- **Name:** Franklin Afolabi
- **Task Completed:**
- **Date and Time:** September 21 1125

## Terraform Code 
```hcl
# Module for data-stores/mysql
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

resource "aws_db_instance" "example" {
    identifier_prefix ="terraform-up-and-running"
    allocated_storage = 10
    instance_class = "db.t3.micro"
    skip_final_snapshot = true
    
    # Enable backups
    backup_retention_period = var.backup_retention_period

    # If specified, this DB will be a replica
    replicate_source_db = var.replicate_source_db

    # Only set these params if replicate_source_db is not set
    engine = var.replicate_source_db == null ? "mysql" : null
    db_name = var.replicate_source_db == null ? var.db_name : null
    username = var.replicate_source_db == null ? var.db_username : null
    password = var.replicate_source_db == null ? var.db_password : null
}

# Variables for the prod data-stores
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

# Outputs for the prod data-stores
output "primary_address" {
    value = module.mysql_primary.address
    description = "Connect to the primary database at this endpoint"
}

output "primary_port" {
    value = module.mysql_primary.port
    description = "The port the primary database is listening on"
}

output "primary_arn" {
    value = module.mysql_primary.arn
    description = "The ARN of the primary database"
}

output "replica_address" {
    value = module.mysql_replica.address
    description = "Connect to the replica database at this endpoint"
}

output "replica_port" {
    value = module.mysql_replica.port
    description = "The port the replica database is listening on"
}


output "replica_arn" {
    value = module.mysql_replica.arn
    description = "The ARN of the replica database"
}

# Main configuration for the primary and replica databases in two separate regions
provider "aws" {
    region = "us-east-2"
    alias = "primary"
}

provider "aws" {
    region = "us-west-1"
    alias = "replica"
}

module "mysql_primary" {
    source = "../../../../modules/data-stores/mysql"
    
    providers = {
        aws = aws.primary
    } 

    db_name = "prod_db"
    db_username = var.db_username
    db_password = var.db_password

    # Must be enabled to support replication
    backup_retention_period = 1
}

module "mysql_replica" {
    source = "../../../../modules/data-stores/mysql"

     providers = {
        aws = aws.replica
    } 

    # Make this a replica of the primary
    replicate_source_db = module.mysql_primary.arn        
}

terraform {
  backend "s3" {
    bucket = "tf-frankfolabi"
    key = "prod/data-stores/mysql/terraform.tfstate"
    region = "us-east-2"

    dynamodb_table = "tf-locks"
    encrypt = true
  }
}


```
## Architecture 

[Name](link to image in S3 bucket)
