### Name: God'sfavour Braimah
### Date: 12/12/24
### Time: 10:30pm
 ### Activity
# Day 9: Continuing Reuse of Infrastructure with Modules

## Overview
This is Day 9 of the **Terraform 30-Day Challenge**, where we explored advanced features of Terraform modules. Building on the foundational knowledge from Day 8, we enhanced our understanding and implementation of reusable infrastructure with:

- **Module Versioning**
- **Support for Multiple Environments**
- **Nested Modules**

By the end of this task, the modules were refactored to support different environments (dev, staging, production) and versioning, ensuring modular and maintainable infrastructure.

## Tasks Completed

### Reading
- **Chapter 4** (Pages 115-139):
  - "Module Gotchas"
  - "Module Versioning"

### Videos Watched
- Video 38: "Terraform module - Scope"
- Video 39: "Terraform module - Public Registry"
- Video 40: "Terraform module - Versioning"

### Enhancements
1. **Added Multi-Environment Support**:
   - Extended the module to deploy VPC and subnets across dev, staging, and production environments.

2. **Enabled Module Versioning**:
   - Refactored the modules to support versioning for better stability and controlled updates.

3. **Nested Modules**:
   - Improved module reusability and organization by introducing nested module structures.

## Example Code

### Main Configuration (`main.tf`):
```hcl
module "vpc" {
  source = "git::https://github.com/GfavourBraimah/vpc_modules"
  cidr_block        = var.vpc_cidr_block
  vpc_name          = var.vpc_name
  subnet_cidr       = var.subnet_cidr
  availability_zone = var.availability_zone
  subnet_name       = var.subnet_name
}
```

### Variables (`variables.tf`):
```hcl
variable "vpc_cidr_block" {}
variable "vpc_name" {}
variable "subnet_cidr" {}
variable "availability_zone" {}
variable "subnet_name" {}
```

### Enhanced Features
- **Version Control:** Managed versions for the VPC module.
- **Multiple Environments:** Separated configurations for dev, staging, and production.

## Summary
Day 9 was a significant step forward in mastering Terraform modules, focusing on versioning and reuse across environments. These practices ensure that infrastructure management is scalable, modular, and maintainable, aligning with industry best practices.
