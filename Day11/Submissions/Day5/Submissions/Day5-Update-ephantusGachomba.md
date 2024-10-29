```markdown
## Terraform State

Terraform State records information about the infrastructure created by Terraform in a state file. By default, this state file is stored locally on the user's machine.

### Problems with Local State Storage

1. **Locking State Files**: Without locking, if two team members run Terraform at the same time, it can lead to race conditions as multiple processes make concurrent updates to the state files. This can cause conflicts, data loss, and state file corruption.

2. **Isolating State Files**: When changes are made in different environments (e.g., test or prod), having all infrastructure defined in the same state can cause issues.

3. **Shared Storage for State Files**: Team members cannot access state files if they are stored locally.

### Issues with Storing State Files in Shared Storage (e.g., Git)

Storing Terraform state in version control is not recommended for the following reasons:

1. **Manual Errors**: It's easy to forget to pull down or update the latest changes from version control, leading to potential conflicts or outdated states.
   
2. **Locking**: Version control systems do not provide any locking mechanism to prevent two team members from running `terraform apply` on the same state file simultaneously.

3. **Secrets Exposure**: All data in Terraform state files is stored in plain text, potentially exposing sensitive information.

## Managing State Across Teams

To manage Terraform state across teams, use Terraform’s built-in support for **remote backends**.

### Benefits of Remote Backends

Remote backends solve the following issues:

1. **Manual Errors**: Terraform automatically loads the state file from the remote backend every time you run `plan` or `apply`, and automatically stores the state file in that backend after each `apply`, minimizing the chance of manual error.

2. **Locking**: Most remote backends natively support locking.

3. **Secrets Protection**: Most remote backends natively support encryption in transit and at rest for the state file.

## Activity: Deploy Infrastructure and Inspect the Terraform State File

- **Configure Remote State Storage**: Use AWS S3 or another cloud provider.
- **Check on VSCode**: Done.

### Limitations with Terraform's Backends

1. **Two-Step Process**:
   - a. Write Terraform code to create the S3 bucket and DynamoDB table, and deploy that code with a local backend.
   - b. Go back to the Terraform code, add a remote backend configuration to use the newly created S3 bucket and DynamoDB table, and run `terraform init` to copy your local state to S3.
   - (Same process applies when deleting.)

2. **Backend Block Limitations**: The backend block in Terraform does not allow you to use any variables or references.

## State File Isolation

Having separate environments ensures isolation from one another.

### 1. Isolation via Workspaces

Terraform workspaces allow you to run `terraform workspace new` and deploy a new copy of the exact same infrastructure while storing the state in a separate file.

#### Limitations of Terraform Workspaces

- i) The state files for all of your workspaces are stored in the same backend.
- ii) Workspaces are not visible in the code or on the terminal unless you run `terraform workspace` commands.
- iii) Due to the above two points, workspaces can be error-prone. The lack of visibility makes it easy to forget which workspace you're in and accidentally deploy changes to the wrong one.

### 2. Isolation via File Layout

- Place the Terraform configuration files for each environment into a separate folder.
- Configure a different backend for each environment, using different authentication mechanisms and access controls.
- At the top level, there are separate folders for each “environment.”

#### Advantages of Isolation via File Layout

- i) Clear code/environment layout.
- ii) Isolation.

#### Disadvantages of Isolation via File Layout

- i) Working with multiple folders.  
  *Solution*: Use Terragrunt to run commands across multiple folders concurrently using the `run-all` command.
  
- ii) Copy/paste.
- iii) Resource dependencies (difficult to manage across different folders).
```
