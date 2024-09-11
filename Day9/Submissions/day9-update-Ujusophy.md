# Day 9: Continuing Reuse of Infrastructure with Modules

## Participant Details

- **Name:** Njoku Ujunwa Sophia
- **Task Completed:** Deploy multiple versions of the module in different environments.
- **Date and Time:** 09/03/2024 12:28 PM 

## main.tf 
```hcl
module "ec2_instance" {
  source = "github.com/Ujusophy/Terraform-module//terraform-modules/ec2-instance?ref=v1.0.0"
  instance_type  = var.instance_type
  region = var.region
}
```
