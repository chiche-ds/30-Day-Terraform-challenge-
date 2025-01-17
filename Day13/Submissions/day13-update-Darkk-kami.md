# Day 13: Managing Sensitive Data in Terraform

## Participant Details

- **Name:** Dwayne Chima
- **Task Completed:** Implemented secure secrets management using AWS Secrets Manager and integrated it into Terraform workflows.
- **Date and Time:** 13th Dec 2024 5:10pm

## Terraform Code 
```hcl
data "aws_secretsmanager_secret" "secret" {
  name = "mysecuresecret"
}

data "aws_secretsmanager_secret_version" "secret_version" {
  secret_id = data.aws_secretsmanager_secret.secret.id
}

locals {
  secret_data = jsondecode(data.aws_secretsmanager_secret_version.secret_string)
}

resource "aws_instance" "web_server" {
  instance_type          = var.instance_type
  ami                    = data.aws_ami.ubuntu.id
  subnet_id              = var.public_subnets[0].id
  vpc_security_group_ids = [var.web_sg.id]

  user_data = <<-EOT
    #!/bin/bash
    sudo apt update -y
    sudo apt upgrade -y
    sudo apt install -y nginx
    sudo systemctl start nginx
    sudo systemctl enable nginx
    echo "<h1>Hello from ${local.secret_data.hello_text}</h1>" | sudo tee /var/www/html/index.html
  EOT
}
```
- The configuration dynamically uses the hello_text value retrieved from AWS Secrets Manager in the Nginx setup script.
- This approach ensures sensitive data is not hardcoded into the Terraform configuration and our output values are masked
![image](https://github.com/user-attachments/assets/ef854c2c-6b35-466f-8a6a-42f3739c58ad)
