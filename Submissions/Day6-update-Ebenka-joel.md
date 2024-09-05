# Day 6: Understanding Terraform State

## Participant Details

- **Name:** Ebenka christian 
- **Date and Time:** 31-08-2024 at 06:00 am
- **Task Completed:** 

- Deploy infrastructure and inspect the Terraform state file.

tfstate of webapp deploy

```bash
{
  "version": 4,
  "terraform_version": "1.8.3",
  "serial": 29,
  "lineage": "ccfbf7dd-024f-b2be-0350-500badc49c13",
  "outputs": {},
  "resources": [],
  "check_results": null
}

```

- Best practice in order to Configure remote state storage using AWS S3 or another cloud provider.
we will configure an s3 bucket to store the state file and a dynamotable to lock it

```bash

terraform {
  backend "s3" {
    bucket = "30-days-challenge-joel"
    key    = "day5-Scaling-Infrastructure"
    region = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

```
Other best practices are

  1- Enable Encryption: Ensure your state files    are encrypted both in transit and at rest to protect sensitive information1.
  2- Implement Access Control: Restrict access to your state files using IAM policies to prevent unauthorized access1.
  3-Enable Versioning: Use versioning on your S3 bucket to keep track of changes and allow rollback if necessary1.
  4- Use File Locking: Prevent concurrent modifications by enabling state locking with DynamoDB or similar services2.
  5- Separate Configuration Files: Organize your Terraform configuration into logical groupings. For example, use separate files for different resource types like network.tf, instances.tf, and backend.tf