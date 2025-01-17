Day 8: Reusing Infrastructure with Modules
Name: Udeh Samuel Chibuike
Task Completed:  Built a basic Terraform module for a common infrastructure component, an EC2 instance.
Date and Time: 12/30/2024 10:48am


provider "aws" {
  region = "us-east-1"
}

module "ec2_instance" {
  source        = "./modules/ec2_instance"
  ami_id        = "ami-01816d07b1128cd2d"
  instance_type = "t2.micro"
}