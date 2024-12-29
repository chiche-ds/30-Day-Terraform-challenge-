## Day 3: Deploying Basic Infrastructure with Terraform

**Name**: Steve Yonkeu

**Date**: 03/12/2024

**Time**: 10:34am

**Task Completed**:

-   Deployed a basic web server using Terraform.
-   Configured the AWS CLI and VSCode with the AWS plugin.
-   Created an architecture diagram.

### Terraform Code

```hcl
provider "aws" {
  region  = "us-east-1"
  profile = "terraform_learner"
}

resource "aws_vpc" "day_3" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "day_3_vpc"
  }
}

resource "aws_internet_gateway" "day_3" {
  vpc_id = aws_vpc.day_3.id
  tags = {
    Name = "day_3_igw"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.day_3.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"
  tags = {
    Name = "day_3_public_subnet"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.day_3.id
  tags = {
    Name = "day_3_public_route_table"
  }
}

resource "aws_route" "internet_access" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.day_3.id
}

resource "aws_route_table_association" "public_subnet_association" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "web_sg" {
  vpc_id = aws_vpc.day_3.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "day_3_web_sg"
  }
}

resource "aws_instance" "learn_tf_ec2" {
  ami                    = "ami-0c02fb55956c7d316"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name = "day_3_ec2"
  }

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install httpd -y
              sudo systemctl start httpd
              sudo systemctl enable httpd
              echo "<h1>Welcome to Terraform</h1>" > /var/www/html/index.html
              EOF
}

output "webserver_ip" {
  value       = aws_instance.learn_tf_ec2.public_ip
  description = "Public IP of the EC2 instance"
}
```

### Architecture Diagram

![30days_day3 drawio](https://github.com/user-attachments/assets/f24d2465-d141-4627-b32c-7d06fec01314)

## Blog Post

-   [Day 3: Deploying Basic Infrastructure with Terraform](https://dev.to/yokwejuste/day-03-deploying-basic-infrastructure-with-terraform-1acm)
