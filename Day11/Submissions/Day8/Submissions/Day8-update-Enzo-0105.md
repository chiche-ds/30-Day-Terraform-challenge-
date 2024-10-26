# Day 8: Reusing Infrastructure with Modules

## Participant Details

- **Name:** Salako Lateef
- **Task Completed:** Built a basic Terraform module for an ec2 
- **Date and Time:** 2024-10-03 21:54 PM

## main.tf 
```
module "instance" {
  source = "terraform-aws-modules/ec2-instance/aws"

  instance_type = "t2.micro"
  ami      = "ami-0e86e20dae9224db8"
  subnet_id = "subnet-03cb68d25e5198c95"
  key_name = "minikube"
  vpc_security_group_ids = ["sg-0ed7b0e6d5df0a363"]
}
```
