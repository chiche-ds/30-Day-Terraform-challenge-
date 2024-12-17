# Day 16: Manual Testing of Terraform Code
## Participant Details

- **Name:** Dwayne Chima
- **Task Completed:** Performed manual testing on terraform configuration.
- **Date and Time:** 17th Dec 2024 11:05 am


## Key Terraform Commands for Manual Testing

### 1. terraform init
Initialize the working directory containing Terraform configuration files.
```bash
terraform init

terraform init -backend=false     # Skip backend initialization
terraform init -upgrade           # Upgrade provider and module versions
terraform init -input=false       # Disable interactive prompts
```

### 2. terraform fmt
Format and standardize Terraform configuration files.

```bash
# Check formatting without modifying files
terraform fmt -check

# Automatically fix formatting
terraform fmt -recursive
```

### 3. terraform validate
Validate configuration files for syntax and internal consistency.
```bash
# Basic validation
terraform validate

# Detailed validation with specific checks
terraform validate -json           # Machine-readable output
```

### 4. terraform plan
Generate a detailed execution plan for infrastructure changes.

```bash
# Standard plan
terraform plan

# Advanced plan options
terraform plan -out=tfplan         # Save plan to file
terraform plan -refresh-only       # Refresh state without planning changes
```

### 5. terraform show
Inspect current infrastructure state and resource configurations.
```bash
# Display full state
terraform show

# Output in JSON format
terraform show -json

# Show specific resource details
terraform show -json aws_instance.web
```
### 6. terraform state Management
Manage and manipulate Terraform state manually.
```bash
# List resources in state
terraform state list

# Show specific resource details
terraform state show aws_instance.web

# Remove resources from state
terraform state rm aws_instance.web
```

## Manual Testing Workflow

### Pre-Deployment Checklist

1. **Configuration Validation**
   - Run `terraform fmt` to standardize code
   - Execute `terraform validate` for syntax checks

2. **Dependency and Provider Verification**
   - Check `terraform init` output for provider versions
   - Verify required provider versions and update if necessary

3. **Execution Plan Review**
   - Run `terraform plan` in sandbox environment
   - Carefully examine proposed changes


