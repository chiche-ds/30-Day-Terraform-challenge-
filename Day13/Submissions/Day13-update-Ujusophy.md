# Day 13: Managing Sensitive Data in Terraform


## Participant Details

- **Name:** Njoku Ujunwa Sophia
- **Task Completed:** Implement secure management of sensitive data and ensure that sensitive data is properly masked and encrypted in Terraform state files
- **Date and Time:** 9/03/2024 06:48 PM 


For API keys and tokens, we can use environment variables instead of hardcoding them in the Terraform files
```
export AWS_ACCESS_KEY_ID="your_access_key_id"
export AWS_SECRET_ACCESS_KEY="your_secret_access_key"
```
And you can reference these environment variables
```hcl
provider "aws" {
  region                  = var.region
  access_key              = var.access_key
  secret_key              = var.secret_key
}
```
