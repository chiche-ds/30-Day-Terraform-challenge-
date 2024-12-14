### Name: God'sfavour Braimah
### Task: Day 11: Terraform Conditionals 
### Date: 12/14/24
### Time: 12:55pm
 ### Activity
# Terraform Conditional Resource Creation

This project demonstrates how to use **conditional expressions** in Terraform to dynamically create AWS S3 buckets based on input variables. This approach ensures efficient and flexible infrastructure provisioning by deploying resources only when required.

---

## Overview

This Terraform configuration:
- Creates an S3 bucket for logging if `enable_logging` is set to `true`.
- Creates an S3 bucket for backups if `create_backup` is set to `true`.
- Ensures unique bucket names using the `random_pet` resource.
- Outputs the names of the created buckets dynamically based on the input variables.

---

## Prerequisites
- Terraform installed on your local machine.
- AWS CLI configured with appropriate permissions to create S3 buckets.
- An active AWS account.

---

## Input Variables
| Variable         | Description                                    | Type    | Default |
|------------------|------------------------------------------------|---------|---------|
| `enable_logging` | Enables the creation of a logging S3 bucket   | `bool`  | `true`  |
| `create_backup`  | Enables the creation of a backup S3 bucket    | `bool`  | `false` |

---

## Provider Configuration
```hcl
provider "aws" {
  region = "us-east-1"
}
```

---

## Resources
### S3 Bucket for Logging (Conditional)
```hcl
resource "aws_s3_bucket" "logging_bucket" {
  count = var.enable_logging ? 1 : 0
  bucket = "logging-bucket-${random_pet.name.id}"
}
```

### S3 Bucket for Backups (Conditional)
```hcl
resource "aws_s3_bucket" "backup_bucket" {
  count = var.create_backup ? 1 : 0
  bucket = "backup-bucket-${random_pet.name.id}"
}
```

### Random ID Generator
```hcl
resource "random_pet" "name" {}
```

---

## Outputs
### Logging Bucket Name
```hcl
output "logging_bucket_name" {
  value       = var.enable_logging ? aws_s3_bucket.logging_bucket[0].bucket : null
  description = "Logging bucket name (if created)"
}
```

### Backup Bucket Name
```hcl
output "backup_bucket_name" {
  value       = var.create_backup ? aws_s3_bucket.backup_bucket[0].bucket : null
  description = "Backup bucket name (if created)"
}
```

---

## How to Test
1. Initialize Terraform:
   ```bash
   terraform init
   ```

2. Apply the configuration with default variables:
   ```bash
   terraform apply
   ```

3. To test specific conditions, modify the input variables:
   - Enable both logging and backup buckets:
     ```hcl
     variable "enable_logging" {
       default = true
     }

     variable "create_backup" {
       default = true
     }
     ```

   - Reapply Terraform:
     ```bash
     terraform apply
     ```

4. Destroy the infrastructure:
   ```bash
   terraform destroy
   ```

---

## Key Learnings
- **Conditional Expressions:** Efficiently control resource creation using expressions like `count = var.enable_logging ? 1 : 0`.
- **Dynamic Outputs:** Outputs adapt based on resource creation, ensuring meaningful results.
- **Resource Uniqueness:** Utilized `random_pet` to ensure globally unique S3 bucket names.

---

## Notes
- Ensure that the AWS region specified in the provider block is accurate.
- S3 bucket names must be globally unique, and `random_pet` helps achieve this.
