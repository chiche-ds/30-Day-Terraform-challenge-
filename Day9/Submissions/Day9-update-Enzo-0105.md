## Day 9:Continuing Reuse of Infrastructure with Modules

## Participant Details

- **Name:** Salako Lateef 
- **Task Completed:** Enhancing terraform module 
- **Date and Time:** 2024-08-29 08:54 AM GMT

## main.tf 

```
module "instance" {
  source = "terraform-aws-modules/ec2-instance/aws"
  version = var.env

  instance_type = var.instance_type
  ami      = var.ami
  subnet_id = "var.subnet
  key_name = "minikube"
  vpc_security_group_ids = var.sg
```
