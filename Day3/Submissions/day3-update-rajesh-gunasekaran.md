**Name: ** Rajesh Gunasekaran

**Task Completed: ** Watch video 11,12,13

** Read chapter 2

** Date: ** 23-07-2025

main.tf

```hcl
provider "aws" {
  region = "eu-west-1"
  }
resource "aws_vpc" "name" {
  cidr_block = "10.0.0.0/16"
  tags = {
    "Name" = "my-vpc"
  }
}

resource "aws_subnet" "main" {
  vpc_id = aws_vpc.name.id
  cidr_block = "10.0.1.0/24"

  tags = {
    "Name" = "Main" 
  }
}

resource "aws_instance" "xyz" {
  ami = "ami-00e4b38ff40625624"
  instance_type = "t2.micro"
  subnet_id = aws_subnet.main.id
  tags = {
    "Name" = "rajesh-ec2-instance"
  }
}
