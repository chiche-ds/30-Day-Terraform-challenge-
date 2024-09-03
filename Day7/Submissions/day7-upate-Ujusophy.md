# Day 7: Understanding Terraform State

## Participant Details
- **Name:** Ujunwa Njoku Sophia
- **Task Completed:** : Workspace Layout and File Layouts
- **Date and Time:** 2024-09-03 09:07am

## Start by initializing the Terraform project if it’s not already done:
 ```hcl
terraform init
 ```
## Create workspaces
 ```hcl
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod
 ```
## Switch to a specific workspace
 ```hcl
terraform workspace select dev
 ```
