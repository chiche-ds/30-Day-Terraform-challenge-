# Day 8: Reusing Infrastructure with Modules

## Participant Details

- **Name:** Vijayaraghavan Vashudevan
- **Task Completed:** Learnt - Understand how to create reusable modules in Terraform, define input variables, and output values from modules and terraform module sources.
- **Date and Time:** 03-09-2024 at 22:19 pm IST

### main.tf
```
resource "aws_instance" "web" {
  ami                    = var.ami
  instance_type          = var.size
  subnet_id              = var.subnet_id
  vpc_security_group_ids = var.security_groups

  tags = {
    "Name"        = "Server from Module"
    "Environment" = "Training"
  }
}
```
### variables.tf
```
variable "ami" {}
variable "size" {
  # default = "t3.micro"
}
variable "subnet_id" {}
variable "security_groups" {
  type = list(any)
}
```
### main.tf
```
module "server" {
  source          = "./modules/server"
  ami             = data.aws_ami.ubuntu.id
  size            = "t3.micro"
  subnet_id       = aws_subnet.public_subnets["public_subnet_3"].id
  security_groups = [aws_security_group.vpc-ping.id, aws_security_group.ingress-ssh.id, aws_security_group.vpc-web.id]
}

output "size" {
value = module.server.size
}

output "public_ip" {
value = module.server.public_ip
}

```
### output.tf
```bash
output "public_ip" {
description = "IP Address of server built with Server Module"
value = aws_instance.web.public_ip
}
output "public_dns" {
description = "DNS Address of server built with Server Module"
value = aws_instance.web.public_dns
}
output "size" {
description = "Size of server built with Server Module"
value = aws_instance.web.instance_type
}
```
