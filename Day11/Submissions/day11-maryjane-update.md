# Day 11: Understanding Terraform Conditionals

## Participant Details

- **Name:** Maryjane Enechukwu
- **Task Completed:** Conditionals with Terraform
- **Date and Time:** 2024-10-20 6:18pm


# main.tf
```

# Define my EC2 instances (Blue/Green environments)
resource "aws_instance" "web_app_blue" {
  ami           = "ami-06b21ccaeff8cd686" # Blue environment
  instance_type = "t2.micro"
  tags = {
    Name = "WebAppBlue"
  }
}

resource "aws_instance" "web_app_green" {
  ami           = "ami-06b21ccaeff8cd686" # Green environment
  instance_type = "t2.micro"
  tags = {
    Name = "WebAppGreen"
  }
}

resource "aws_vpc" "app_vpc" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "app-vpc"
  }
}

# Define Security Group for Load Balancer
resource "aws_security_group" "lb_sg" {
  name        = "lb-sg"
  description = "Allow HTTP inbound traffic"
  vpc_id      = aws_vpc.app_vpc.id

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

  tags = {
    Name = "lb-sg"
  }
}

# Define Subnets for the Load Balancer
resource "aws_subnet" "app_subnet" {
  count = 2
  vpc_id     = aws_vpc.app_vpc.id
  cidr_block = cidrsubnet(aws_vpc.app_vpc.cidr_block, 8, count.index)

    availability_zone = element(["us-east-1a", "us-east-1b"], count.index)


  tags = {
    Name = "app-subnet-${count.index}"
  }
}


# Define Load Balancer and Target Groups
resource "aws_lb" "app_lb" {
  name               = "app-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = aws_subnet.app_subnet[*].id
}

resource "aws_lb_target_group" "blue_tg" {
  name     = "blue-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.app_vpc.id

  
}

resource "aws_lb_target_group" "green_tg" {
  name     = "green-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.app_vpc.id


  }
```

# variable.tf 

```
# variables.tf
variable "instance_type" {
  description = "Type of instance to use for EC2"
  default     = "t2.micro"
}

variable "ami" {
  description = "Amazon Machine Image ID"
  default     = "ami-06b21ccaeff8cd686"
}


variable "security_groups" {
  description = "Security group IDs for the EC2 instances"
  type        = list(string)
  default     = ["sg-0c393266741c7f06a"]
}

variable "vpc_id" {
  description = "The VPC ID"
  default     = "vpc-03a402beb079dd496"
}

variable "subnets" {
  description = "The Subnet IDs for the load balancer"
  type        = list(string)
  default     = ["subnet-0846e4641e585a3df", "subnet-0b80d1672c1d6452a"]
}

variable "canary_percent" {
  description = "Percentage of traffic to route to the canary release"
  type        = number
  default     = 10
}
```

# provider.tf 
```

# provider.tf
provider "aws" {
  region = "us-east-1"
}

```