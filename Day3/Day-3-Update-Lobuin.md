# Day 3: Deploying Basic Infrastructure with Terraform

## Task Description

1. **Reading**: i have read Chapter 2 of "Terraform: Up & Running" by Yevgeniy Brikman, focusing on "Deploying a Single Server" and "Deploying a Web Server."
2. **Udemy Videos**: i have Watched the following videos:
   - Video 11: "Terraform Plug-in Based Architecture"
   - Video 12: "Provider Block"
   - Video 13: "Terraform Resource Block"
3. **Activity**: 
   - I have Deployed a basic web server using Terraform on AWS
   - I have Designed an architecture diagram for my web server using [draw.io](https://app.diagrams.net/).
   - [S3 Bucket Object URL for my architecture diagram web server ](https://deyobucket.s3.amazonaws.com/deplying+simple+server+.drawio.png)
```hcl
    provider "aws" {
  region = "us-east-2"
}

resource "aws_instance" "terraform_instance" {
  ami                         = "ami-0fb653ca2d3203ac1"
  instance_type               = "t2.micro"
  vpc_security_group_ids      = [aws_security_group.instance.id]
  user_data                   = <<-EOF
    #!/bin/bash
    echo "Hello, World" > index.html
    nohup busybox httpd -f -p 8080 &
  EOF
  user_data_replace_on_change = true
  tags = {
    Name = "demo_web_server"
  }
}

resource "aws_security_group" "instance" {
  name = "terraform-example-instance"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

  
