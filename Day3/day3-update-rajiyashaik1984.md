# Day 3 : Deploy basic infrastructure-terraform

## Participant Details
- **Name: ** Rajiya Shaik
- **Task Completed: ** Watch video 11,12,13

    ** Read chapter 2

  ** Date: ** 22-08-2024

  

  main.tf
  ```bash
  provider "aws" {
    region = "us-east-1"
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
    ami = "ami-066784287e358dad1"
    instance_type = "t2.micro"
    subnet_id = aws_subnet.main.id
    tags = {
      "Name" = "my-instane"
    }
  }
  ```
  