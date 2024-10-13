
# Day 3: Deploying Basic Infrastructure with Terraform

## Participant Details

- **Name:** William Maina
- **Task Completed:** Deploying Basic Infrastructure with Terraform
- **Date and Time:** 2024-10-04 at 7:00 am

## Terraform Code 

main.tf
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
              # Update the system and install Apache HTTP server (apache2)
              apt-get update -y
              apt-get install -y apache2
              # Enable Apache to start on boot
              systemctl enable apache2
              # Start Apache service
              systemctl start apache2
              # Create a simple HTML page for testing
              echo "<html><h1>Apache Web Server on Ubuntu is Running</h1></html>" > /var/www/html/index.html
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
```
output.tf
```bash
output "web_instance_ip" {
  value = aws_instance.test.public_ip
}
