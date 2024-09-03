# Day 13: Managing Sensitive Data in Terraform


## Participant Details

- **Name:** Njoku Ujunwa Sophia
- **Task Completed:** Implement secure management of sensitive data and ensure that sensitive data is properly masked and encrypted in Terraform state files
- **Date and Time:** 9/03/2024 06:48 PM 

### Using AWS Secret Manager
Before you can use a secret, you need to store it in AWS Secrets Manager.
```
aws secretsmanager create-secret --name MySecret --secret-string "MySecretValue"
```
To access this secret on Terraform, use the `aws_secretsmanager_secret` and `aws_secretsmanager_secret_version` data sources.

```hcl
data "aws_secretsmanager_secret" "my_secret" {
  name = "MySecret"
}

data "aws_secretsmanager_secret_version" "my_secret_version" {
  secret_id = data.aws_secretsmanager_secret.my_secret.id
}

resource "aws_instance" "web_server"{
    ami = "ami-0e86e20dae9224db8"
    instance_type = "t2.micro"
    tags = {
        first = "web_server"
        SecretValue = data.aws_secretsmanager_secret_version.my_secret_version.secret_string
    }
}

output "secret_value" {
  value     = data.aws_secretsmanager_secret_version.my_secret_version.secret_string
  sensitive = true
}
```
