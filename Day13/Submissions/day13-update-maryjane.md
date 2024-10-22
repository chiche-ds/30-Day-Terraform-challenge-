# Day 13: Managing Sensitive Data in Terraform


## Participant Details

- **Name:** Maryjane Enechukwu Chiziterem
- **Task Completed:** Implement secure management of sensitive data and ensure that sensitive data is properly masked and encrypted in Terraform state files
- **Date and Time:** 22/10/2024 06:48 PM 

I created a secret in AWS Secrets Manager that can store sensitive information, such as a database password, API key, or token.

```
hcl

resource "aws_secretsmanager_secret" "db_password" {
  name        = "db-password"
  description = "Database password stored in AWS Secrets Manager"

  tags = {
    Environment = "production"
  }
}
```


data "aws_secretsmanager_secret" "db_password" {
  name = aws_secretsmanager_secret.db_password.name
}

data "aws_secretsmanager_secret_version" "db_password_version" {
  secret_id = data.aws_secretsmanager_secret.db_password.id
}

resource "aws_instance" "app_instance" {
  ami           = "ami-06b21ccaeff8cd686"
  instance_type = "t2.micro"
  
  tags = {
    Name = "AppInstance"
  }

  user_data = <<-EOF
              #!/bin/bash
              export DB_PASSWORD=$(aws secretsmanager get-secret-value --secret-id ${data.aws_secretsmanager_secret_version.db_password_version.secret_string} --query SecretString --output text
              # Other startup scripts
            EOF
}


output "db_password" {
  value     = data.aws_secretsmanager_secret_version.db_password_version.secret_string
  sensitive = true  
}
