Name: CHIBUZO NWOBIA

  Task: Day 3: Deploying Basic Infrastructure with Terraform
   
  Date: 8/22/24

  Time: 06:03am
Deployment of a webserver on a single server

main.tf file carrying my aws provider, AWS EC2 instance reosurce block and security group resource block.

```
provider "aws" {
  region = "us-east-1"  # Replace with your desired region
}

resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Allow HTTP and SSH inbound traffic"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
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
  ami           = "ami-066784287e358dad1"  
  instance_type = "t2.micro"
  key_name      = "my-terraform-key"  


  vpc_security_group_ids = [aws_security_group.web_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y httpd
              sudo systemctl start httpd
              sudo systemctl enable httpd
              echo "Hello Chibuzo's demo page!" > /var/www/html/index.html
            EOF

  tags = {
    Name = "Terraform-Web-Server"
  }
}

output "instance_public_ip" {
  value = aws_instance.web_server.public_ip
}

```
terrafrom.tf file containing the latest version of terraform configurartion.

```terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.63.0"
    }
  }
}
```


webserver showing on my ![browser](C:\Users\c_not\OneDrive\Pictures\Screenshots\Terraform 30 day challenge\demopage.png)
