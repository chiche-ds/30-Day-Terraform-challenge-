
# Day 4: Deploying Web Server Infrastructure with terraform using variables and local
## Participant details 
* Name: Salako Lateef
* Task: Basic web server
* Date: [2/20/2024 20:00]

## variables.tf 
```
variable "ami" {
  type    = string
  default = "ami-0e86e20dae9224db8"
}

variable "subnet" {
  type    = string
  default = "subnet-059d650d330b4584a"
}

variable "type" {
  type    = string
  default = "t2.micro"
}

variable "sg" {
  type    = string
  default = "sg-0d4c0510df5f61e80"
}
```

## main.tf
```
locals {
  name = "web-server"
}

resource "aws_instance" "web-server" {
  ami             = var.ami
  subnet_id       = var.subnet
  instance_type   = var.type
  security_groups = var.sg
  associate_public_ip_address = "true"

  user_data = <<-EOF
  #!/bin/bash 
  sudo apt update -y
  sudo apt install apache2 -y 
  sudo systemctl start apache2 
  EOF

  tags = {
    Name = local.name
  }
}
```
