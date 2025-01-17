## Day 9 Task : Continuing Reuse of Infrastructure with Modules
Otu Udo | December 12 2024 | 8:30 PM 

I learnt how to use module concepts and techniques like
- module versioning
- calling modules in different environemnts like dev, staging and prod



module "vpc" {
  source         = "git::https://github.com/Otumiky/vpc-module"
  vpc_cidr       = "10.0.0.0/16"
  vpc_name       = "my-vpc"
  staging_cidr   = "10.0.1.0/24"
  production_cidr = "10.0.2.0/24"
  staging_az     = "us-east-1a"
  production_az  = "us-east-1b"
}
