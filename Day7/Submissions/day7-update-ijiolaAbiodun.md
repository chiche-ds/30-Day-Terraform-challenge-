## 1. Workspace isolation.
--Useful for quick, isolated tests on the same configuration.

--store your Terraform state in multiple, separate, named workspaces

--challenges::

A module may have only one backend configuration. The backend was previously configured at main.tf:57,3-15.
  comment out one of the config.

b.Error: Backend configuration changed
│ A change in the backend configuration has been detected,
│ which may require migrating existing state.

[resolve by running "terraform init -reconfigure"]

c. Error : Bucket already created and dynamodb.

[Comment the section to create resource of s3 bucket and the dynamodb table.]

## 2.File Layout isolation.

--Useful for production use cases for which you need strong separation between
environments.
--Put the Terraform configuration files for each environment into a separate folder.
--Configure a different backend for each environment, using different authentication mechanisms and access controls:

main.tf:

```hcl
provider "aws" {
  region = "us-east-1"
}

// first step is to create an S3 bucket.
/*resource "aws_s3_bucket" "terraform_state" {
  bucket = "my-bucket-u5484439473"
}
*/

// Enable versioning to the s3 bucket
/*resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}
*/

// second create Server-side encryption as we will store sensitive data
/*resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.terraform_state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
*/

// Third block public access to S3 bucket (It adds a layer of security)
/*resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
*/

// fourth create a dynamodb table to use for locking
// primary key = LockID
/*resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-up-and-running-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
*/

// run terraform init (download provider code)
// terraform apply

// fifth step (add a backend config to your terraform code)
/*terraform {
  backend "s3" {
    bucket = "bucket-2-f439569547"
    key = "global/s3/terraform.tfstate"
    region = "us-east-1"

    dynamodb_table = "terraform-up-and-running-locks"
    encrypt = true
  }
}
*/

// run terraform init again to download provider code and configure terraform backend
// Terraform will automatically detect that you already have a state file locally and
// prompt you to copy it to the new S3 backend

// add a resource
/*
output "s3_bucket_arn" {
    value = aws_s3_bucket.terraform_state.arn
    description = "The ARN of the S3 bucket"
}
*/
/*
output "dynamodb_table_name" {
    value = aws_dynamodb_table.terraform_locks.name
    description = "The name of the DynamoDB table"
}
*/

// run terraform apply (it acquires a lock first)
// new version of s3 bucket is created

// Isolation via Workspaces
// step 1: create an instance/resource example
resource "aws_instance" "web-server" {
    ami           = "ami-0fb653ca2d3203ac1"
    instance_type = "t2.micro"
}

// step 2 : Configure backend config
terraform {
  backend "s3" {
    bucket = "backend-config-storage-43954933"
    key    = "workspaces-example/terraform.tfstate"
    region = "us-east-1"

    dynamodb_table = "terraform-up-and-running-locks"
    encrypt        = true
  }
}

// run terraform init
// terraform init -reconfigure
// terraform apply
// terraform workspace show (to identify the workspace you are currently in)

// create a new workspace
// terraform workspace new example1
// terraform plan (doesn't show any error.Terraform isn’t using the state file from the default workspace and therefore doesn’t see the EC2 Instance was already created there.)

// terraform workspace select example1 (switching workspaces)
```

