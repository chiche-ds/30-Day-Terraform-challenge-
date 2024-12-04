### Name: God'sfavour Braimah
### Task: Day 3: Deploying Basic Infrastructure with Terraform
### Date: 12/4/24
### Time: 10:37am

# Day 3: Deploying Basic Infrastructure with Terraform

## Overview

Today, I deployed a basic web server using Terraform on AWS. This task helped me understand Terraform's provider and resource blocks while getting hands-on experience with deploying infrastructure as code (IaC).

---

## My Terraform Code

Below is the code I used to deploy the infrastructure:

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "web_server_sg" {
  name = "web_server_sg"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web_server" {
  ami           = "ami-0453ec754f44f9a4a" # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.web_server_sg.id]

  user_data = <<-EOF
    #!/bin/bash
    sudo yum update -y
    sudo yum install -y httpd
    sudo systemctl start httpd
    sudo systemctl enable httpd
    echo "Hello, World" > /var/www/html/index.html
  EOF

  tags = {
    Name = "web_server"
  }
}
```

## Architecture Diagram

Here is the architecture of the infrastructure deployed using Terraform:

![alt text](infra_dep.png)

## Web Server Verification

The deployed web server responds with "Hello, World" as shown below:

![alt text](web_server.png)