# Day 6: Understanding Terraform State

- **Name:** Dwayne Chima
- **Task:** Configure remote state storage
- **Date and Time:** 8th Dec 2024 2:00pm


## Architecture Diagram
![state](https://github.com/user-attachments/assets/083a0c83-da34-41b0-ad3e-51cf90122e6d)


- The Terraform State is stored in AWS S3 for persistent storage.
- DynamoDB is used for state locking to prevent race conditions when applying Terraform changes in a multi-team environment.
- This ensures that multiple users or CI/CD pipelines don't overwrite each other’s changes and provides a central source of truth for your infrastructure.

backend.tf
```
# Configure the backend for remote state storage
terraform {
  backend "s3" {
    bucket         = "your-unique-bucket-name"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "lock-table"
    acl            = "bucket-owner-full-control"
  }
}

```

## Challenges Faced
I faced an issue with creating the S3 bucket directly within the Terraform configuration file. This caused the state file to get lost when running the terraform destroy command because the bucket itself was being destroyed as part of the process.


**Solution:** To resolve this, I made sure to create the S3 bucket separately, outside of Terraform, so that it would persist across Terraform runs and wouldn't be destroyed when tearing down infrastructure.


For the state reconfiguration issue, I used terraform state push to manually push the existing local state to the new remote backend.
I also updated the backend configuration using terraform init and the -reconfigure flag to point to the new S3 bucket.


