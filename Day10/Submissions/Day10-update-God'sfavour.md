### Name: God'sfavour Braimah
### Task: Day 10: Loops
### Date: 12/13/24
### Time: 2:35pm
 ### Activity
 # Terraform Configuration for IAM User Creation

## Overview
This project demonstrates how to dynamically create AWS IAM users using Terraform's looping feature (`for_each`). The code utilizes input variables to define a list of usernames and dynamically provisions the specified IAM users in AWS. This approach ensures scalability and reusability while adhering to best practices in Infrastructure as Code (IaC).

---

## Files Included
- **`main.tf`**: Contains the Terraform configuration for creating IAM users.
- **`variables.tf`**: Defines the input variables for the IAM user list.
- **`outputs.tf`**: Outputs the names of the created IAM users.

---

## Features
1. **Dynamic User Creation**:
   - Uses the `for_each` loop to dynamically create IAM users based on the input variable list.

2. **Tagging**:
   - Assigns an `Environment` tag to each IAM user, categorizing them under `Development`.

3. **Output Management**:
   - Outputs a list of created IAM usernames for easy verification.

---

## Prerequisites
- An AWS account.
- Terraform CLI installed.
- AWS CLI configured with appropriate permissions to create IAM users.

---

## Variables
| Name              | Type         | Default                           | Description                        |
|-------------------|--------------|-----------------------------------|------------------------------------|
| `iam_users`       | `list(string)` | `["Zorath", "Kaelix", "Nivara", "Drayven"]` | List of IAM usernames to be created. |

---

## Terraform Configuration
### Provider Configuration
```hcl
provider "aws" {
  region = "us-east-1"
}
```

### Resource: IAM Users
This block dynamically creates IAM users based on the input variable list:
```hcl
resource "aws_iam_user" "users" {
  for_each = toset(var.iam_users) # Ensure unique usernames
  name     = each.key

  tags = {
    Environment = "Development"
  }
}
```

### Output
The output block provides the list of created IAM usernames:
```hcl
output "iam_user_names" {
  description = "List of created IAM user names"
  value       = [for user in aws_iam_user.users : user.name]
}
```

---

## How to Use
1. **Initialize Terraform**:
   Run the following command to initialize the Terraform workspace:
   ```bash
   terraform init
   ```

2. **Plan the Deployment**:
   Preview the changes Terraform will make:
   ```bash
   terraform plan
   ```

3. **Apply the Configuration**:
   Deploy the IAM users:
   ```bash
   terraform apply
   ```
   Confirm by typing `yes` when prompted.

4. **Verify Outputs**:
   After the deployment, Terraform will output the list of created IAM usernames:
   ```
   iam_user_names = [
     "Zorath",
     "Kaelix",
     "Nivara",
     "Drayven"
   ]
   ```

5. **Clean Up Resources**:
   To destroy the created resources, run:
   ```bash
   terraform destroy
   ```
   Confirm by typing `yes` when prompted.

---

## Best Practices
- **Unique Usernames**: The use of `toset` ensures that the IAM usernames are unique.
- **Environment Tagging**: Tags help in categorizing resources, making management easier.
- **Modular Code**: This configuration can be extended or reused for similar deployments.

---

## Notes
- Ensure that your AWS credentials have sufficient permissions to create IAM users.
- Always verify the list of IAM users before applying changes to avoid accidental user creation.

---

## Outputs
| Name               | Description                        |
|--------------------|------------------------------------|
| `iam_user_names`   | List of IAM usernames created by Terraform. |

---

## Conclusion
This project showcases the power of Terraform's looping constructs to simplify and automate resource creation in AWS. By leveraging dynamic configurations, we can create scalable and reusable infrastructure code.
