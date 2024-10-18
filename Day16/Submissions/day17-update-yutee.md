# Day 17: Manual Testing of Terraform Code

## Participant Details

- **Name:** Utibe Okon (yutee)
- **Task Completed:** Explored manual testing
- **Date and Time:** Tue 15th October, 2024 | 1:20 PM GMT+1

Manual testing interraform is quite basic and I have been doing much of that already.
So basically, the terraform workflow involves testing, especially with the plan feature. After writing your configuration files for the first time, do:

## Terraform Code 
```hcl
# spin up a terraform env
terraform init

# confirm correction of syntax and basic rules
terraform validate

# run a plan of the resources to be created
terraform plan

# starts to interact the provider to provision resources
terraform apply

```