# Day 3: Deploying Basic Web Server Infrastructure with terraform 
## Participant details 
* Name: Salako Lateef
* Task: Basic web server
* Date: [2/20/2024 20:00]

## main.tf
```
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web-server" {
  ami             = "ami-0e86e20dae9224db8"
  subnet_id       = "subnet-059d650d330b4584a"
  instance_type   = "t2.micro"
  security_groups = ["sg-0d4c0510df5f61e80"]
  associate_public_ip_address = "true"

  user_data = <<-EOF
  #!/bin/bash 
  sudo apt update -y
  sudo apt install apache2 -y 
  sudo systemctl start apache2 
  EOF

  tags = {
    Name = web
  }
}
```
