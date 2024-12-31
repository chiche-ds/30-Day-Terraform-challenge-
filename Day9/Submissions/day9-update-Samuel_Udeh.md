Day 9: Reusing Infrastructure with Modules
Name: Udeh Samuel Chibuike
Task Completed: I added advanced features to your module from Day 9, such as supporting multiple environments (dev, staging, production) or enabling versioning for the module.infrastructure component, an EC2 instance.
Date and Time: 12/31/2024 4:15pm

module "vpc" {
  source         = "git::https://github.com/SamuelUdeh/my-terraform-project"
  vpc_cidr       = "10.0.0.0/16"
  vpc_name       = "my-vpc"
  staging_cidr   = "10.0.1.0/24"
  production_cidr = "10.0.2.0/24"
  staging_az     = "us-east-1a"
  production_az  = "us-east-1b"
}