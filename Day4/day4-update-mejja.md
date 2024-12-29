# Day 4: Mastering Basic Infrastructure

## Participant Details
- **Name:** Major Mbandi
- **Task Completed:** Mastering Basic Infrastructure with Terraform
- **Date and Time:** 2024-12-04 2241hrs GMT

##   main.tf
```
provider "aws" {
  region     = var.region
  access_key = var.access_key
  secret_key = var.secret_key
}

resource "aws_security_group" "web-server" {
  name        = "web-server"
  description = "Allow incoming HTTP Connections"
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

resource "aws_instance" "web-server" {
  ami             = "ami-02e136e904f3da870"
  instance_type   = "t2.micro"
  key_name        = "MajorLab-key"
  security_groups = ["${aws_security_group.web-server.name}"]
  user_data       = <<-EOF
  #!/bin/bash
sudo su
yum update -y
yum install httpd -y
systemctl start httpd
systemctl enable httpd
echo "<html><h1> Deployed a highly available web app today! I'm beginning to enjoy the benefits of IaC.. </h1></html>" >> /var/www/html/index.html
EOF
  tags = {
    Name = "web_instance"
  }
}

```

## output.tf
```
output "web_instance_ip" {
  value = aws_instance.web-server.public_ip
}
```

## variables.tf
```
variable "access_key" {
  description = "Access kkey to AWS Console"
}
variable "secret_key" {
  description = "Secret key to AWS console"
}
variable "region" {
  description = "Region of AWS VPC"
}
```

## terraform.tfvars
```
region      = "us-east-1"
access_key  = "ACCESS_KEY"
secret_key  = "SECRET_KEY"
```
Ensure you replace the secrets with your secrets i could not share mine here.