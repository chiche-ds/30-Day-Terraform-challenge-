# Day 17: Manual Testing of Terraform Code

## Participant Details

- **Name:** Omekwu Victor Ebube  
- **Task Completed:** Performed manual testing on Terraform configurations to verify resource creation and behavior, and cleaned up afterward.  
- **Date and Time:** 18-November-2024 at 2:00 PM WAT.
---
## Key Terraform Commands for Manual Testing

### 1. **terraform init**
Initialize the working directory containing Terraform configuration files. This command downloads the necessary providers and sets up the backend.
```bash
terraform init
```

### 2. **terraform plan**
Generate an execution plan. This step allows you to review changes that will be made to your infrastructure before applying them. Manually review the plan output to ensure no unintended changes are being made.
```bash
terraform plan
```

### 3. **terraform apply**
Apply the changes to your infrastructure. Always manually confirm the changes when using this command to ensure the changes are intentional.
```bash
terraform apply
```

### 4. **terraform show**
Inspect the current state of your infrastructure. This command can be used to manually check that the resources are provisioned as expected after applying changes.
```bash
terraform show
```

### 5. **terraform validate**
Validate the configuration files to ensure they are syntactically correct. This helps catch simple errors early in the process.
```bash
terraform validate
```

## Best Practices for Manual Testing
- **Review the Terraform plan output carefully** to ensure there are no unexpected changes.
- **Simulate changes in a staging environment** before applying them to production.
- **Manually verify resource configurations** to ensure they meet security and compliance standards.

By following these steps, manual testing with Terraform ensures that your infrastructure remains secure, stable, and aligned with best practices.
