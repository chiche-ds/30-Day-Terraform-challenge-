# Day 3: Deploying Basic Infrastructure with Terraform

Name: Major Mbandi
Task Completed: Deploying a Single Server" and "Deploying a Web Server"
Date: 12-03-24
Blog link:https://medium.com/@majorkiema.mk/getting-started-with-terraform-a-beginners-guide-to-deploying-your-first-server-05722f05d4a2
social media post: https://x.com/majorkiema1/status/1864092251573366859


### Terraform Code 
```python
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
echo "<html><h1> Welcome to Terraform IaC tool by Major... </h1></html>" >> /var/www/html/index.html
EOF
  tags = {
    Name = "web_instance"
  }
}```