# Day 7: Understanding Terraform State

## Participant Details
- **Name:** Dwayne Chima
- **Task Completed:** Understanding Terraform state
- **Date and Time:** 9th Dec 2024 3:00pm

## Create workspaces
 ```
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod
 ```

### Switch to a specific workspace
 ```
terraform workspace select dev
 ```

## Folder Structure on File isolation
```
# File Layout Isolation Folder Structure

# Root Directory
├── modules
│   ├── network
│   ├── compute
│   └── storage
├── environments
│   ├── dev
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── prod
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── staging
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
```


