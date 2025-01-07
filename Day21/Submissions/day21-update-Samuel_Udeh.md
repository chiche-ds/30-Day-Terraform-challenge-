Day 21: Workflow for Deploying Infrastructure Code
Name: Udeh Samuel Chibuike
Task Completed: Workflow for Deploying Application Code
Date and Time: 7/1/2025 4:28am

# main.tf

provider "aws" {
    region = "us-east-1"
}

resource "aws_instance" "example" {
    ami = "ami-01816d07b1128cd2d"
    instance_type = "t2.micro"

    tags = {
        Name = "ExampleInstance"
    }
  
}