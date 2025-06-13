Day 26: Build a Scalable Web Application with Auto Scaling on AWS
Name: Udeh Samuel Chibuike
Task Completed: Build a Scalable Web Application with Auto Scaling on AWS
Date and Time: 15/1/2025 11:34pm

module "vpc" {
  source             = "module//vpc"
  cidr_block         = "10.0.0.0/16"
  public_subnets     = ["10.0.1.0/24", "10.0.2.0/24"]
  availability_zones = ["us-east-1a", "us-east-1b"]
  vpc_name           = "two-tier-vpc"
}

module "asg" {
  source          = "module//asg"
  name_prefix     = "web-tier"
  image_id        = "ami-045xxxxxxxxxxx"
  instance_type   = "t2.micro"
  security_groups = module.vpc.asg_sg_id
  subnets         = module.vpc.public_subnets
  desired_capacity = 2
  min_size        = 1
  max_size        = 3
  target_group_arn = module.alb.target_group_arn
  user_data       = var.user_data
  
}

module "alb" {
  source          = "module//elb"
  name            = "web-alb"
  security_groups = module.vpc.alb_sg_id
  subnets         = module.vpc.public_subnets
  vpc_id          = module.vpc.vpc_id
}