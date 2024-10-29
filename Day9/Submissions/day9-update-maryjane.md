# Day 9: Continuing Reuse of Infrastructure with Modules

## Participant Details

- **Name:** Maryjane Enechukwu
- **Task Completed:** Deploy multiple versions of the module in different environments.
- **Date and Time:** 09/03/2024 1:28 PM 


# main.tf
```
hcl

provider "aws" {
  region = "us-east-1"
}


module "ec2_instance" {
  source             = "git::https://github.com/Lumen-jane/Terraform-AWS-EC2-Module.git"
  ami_id             = "ami-06b21ccaeff8cd686"
  instance_type      = "t2.micro"
  instance_name      = "MyEC2Instance"
  subnet_id          = "subnet-08a604e869c0ccd2b"
  security_group_ids = ["sg-0040022bca3d48b8d"]
  environment       = terraform.workspace 
}

output "instance_id" {
  value = module.ec2_instance.instance_id
}

output "public_ip" {
  value = module.ec2_instance.public_ip
}


```