# Day 3: Deploying Basic Infrastructure With Terraform

## Participant Details

- **Name:** Eddie Chem
- **Task Completed:** Completed tasks for Day 3
- **Date and Time:** 08-19-2024 at 8:55 pm

## Terraform Code 

The provided Terraform code sets up an AWS EC2 instance in the `us-east-2` region using a specified Amazon Machine Image (AMI). It configures the instance as a small, low-cost server (`t2.micro`) and runs a simple web server that displays "Hello, World" on port 8080. A security group is also created to allow incoming traffic on port 8080 from any IP address, ensuring that the web server is accessible over the internet.

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

