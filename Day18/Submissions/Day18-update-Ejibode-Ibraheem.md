#  Day 18: Automated Testing of Terraform Code
## Participant Details

- **Name:** Ejibode Ibraheem Adewale
- **Task Completed:** 
- Manual testing  
Automated tests which is of three types:
- Unit tests
- Automated tests
- End-to-end tests

- **Date and Time:** 24/12/2024 11:05 PM

```
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestEC2Instance(t *testing.T) {
    terraformOptions := &terraform.Options{
        TerraformDir: "../modules/ec2_instance",
    }

    defer terraform.Destroy(t, terraformOptions)
    
    terraform.InitAndApply(t, terraformOptions)

    instanceID := terraform.Output(t, terraformOptions, "instance_id")
    assert.NotEmpty(t, instanceID)
}
```


# A workfow
```

name: Terraform CI

on:
  push:
    branches:
      - main

jobs:
  terraform:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v1

      - name: Terraform Init
        run: terraform init

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        run: terraform plan

      - name: Terraform Apply (Auto Approve)
        run: terraform apply -auto-approve
```