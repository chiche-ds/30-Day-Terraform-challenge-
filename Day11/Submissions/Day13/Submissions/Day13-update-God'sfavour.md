### Name: God'sfavour Braimah
### Task: Day 13: Managing Sensitive Data in Terraform
### Date: 12/18/24
### Time: 6:50am
 ### Activity

# Secure Database Deployment with Terraform

This project demonstrates how to securely manage and deploy an AWS RDS database instance using Terraform while safeguarding sensitive information such as usernames and passwords. The credentials are securely stored in AWS Secrets Manager, ensuring they are not hardcoded in Terraform configuration files.

---

## Features

- **Secure Secrets Management**: Database credentials (username and password) are securely retrieved from AWS Secrets Manager.
- **Infrastructure as Code (IaC)**: The database instance is provisioned using Terraform.
- **Encryption**: Sensitive data is encrypted and not exposed in configuration files or Terraform state.
- **AWS RDS MySQL Database**: A secure, managed MySQL database instance is deployed.

---

## Prerequisites

Before using this configuration, ensure you have:

1. **AWS Account**: An active AWS account with permissions to use RDS and Secrets Manager.
2. **Terraform**: Installed and configured Terraform CLI (v1.3 or later recommended).
3. **AWS CLI**: Installed and configured with access keys for your AWS account.
4. **Secrets Created in AWS Secrets Manager**:
    - Create a secret named `database/credentials` with the following structure:

    ```json
    {
      "username": "your_secure_username",
      "password": "your_secure_password"
    }
    ```

---

## Configuration Details

### Terraform Code

```hcl
provider "aws" {
  region = "us-east-1"
}

data "aws_secretsmanager_secret" "db_secret" {
  name = "database/credentials"
}

data "aws_secretsmanager_secret_version" "db_secret_version" {
  secret_id = data.aws_secretsmanager_secret.db_secret.id
}

resource "aws_db_instance" "example" {
  allocated_storage    = 20
  engine               = "mysql"
  instance_class       = "db.t2.micro"
  name                 = "secure_database"
  username             = jsondecode(data.aws_secretsmanager_secret_version.db_secret_version.secret_string)["username"]
  password             = jsondecode(data.aws_secretsmanager_secret_version.db_secret_version.secret_string)["password"]
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true
}
```

---

## Deployment Steps

1. **Clone the Repository**

   Clone this repository to your local machine:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Initialize Terraform**

   Initialize the Terraform working directory:

   ```bash
   terraform init
   ```

3. **Validate the Configuration**

   Validate the Terraform configuration:

   ```bash
   terraform validate
   ```

4. **Plan the Infrastructure**

   Generate and review an execution plan:

   ```bash
   terraform plan
   ```

5. **Apply the Configuration**

   Deploy the database:

   ```bash
   terraform apply
   ```

   Type `yes` when prompted to confirm.

6. **Verify Deployment**

   Check your AWS Console to verify that the RDS instance is created.

---

## Security Considerations

- **Secrets Manager**: Ensure AWS Secrets Manager is configured with proper access controls.
- **Terraform State**: Use a secure backend (e.g., AWS S3 with encryption) to store your Terraform state file.
- **IAM Roles**: Limit IAM permissions to only what is necessary for Terraform to function.

---

## Cleanup

To remove the deployed infrastructure, run:

```bash
terraform destroy
```

Type `yes` when prompted to confirm the destruction.

---
