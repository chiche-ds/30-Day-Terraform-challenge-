# Day 3: Deploying Basic Infrastructure with Terraform

## Participant Details

- **Name:** Mohamed Nourdine
- **Task Completed:** Deploying Basic Infrastructure with Terraform
- **Date and Time:** 2025-01-11 21:00 PM

### main.tf

```bash
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "test" {
  ami                    = "ami-0866a3c8686eaeeba"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.web-server.id]

  tags = {
    Name = "First_EC2"
  }
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              echo "<h1>Welcome to Terraform Deployed Web Server by Mohamed Nourdine</h1>" > /var/www/html/index.html
            EOF
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
output "web_instance_ip" {
  value = aws_instance.test.public_ip
}
```