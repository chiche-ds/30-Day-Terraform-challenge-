# Day 9: Reuse of Infrastructure with Modules

## Participant Details

- **Name:** Kevin Tuei
- **Task Completed:** I completed the process of refactoring Terraform Code to resue Modules to create a Server and a Web Server. I also understood how outputs within the module are referenced by outputs within the root. 
- **Date and Time:** 3/9/2024 11:01PM

## Snippet of Relevant Terraform Code for Main.tf
```hcl
# Terraform Resource Block - To Build EC2 instance in Public Subnet
resource "aws_instance" "web_server_2" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public_subnets["public_subnet_2"].id
  tags = {
    Name = "Web EC2 Server 2"
  }
}

module "server" {
  source          = "./modules/server"
  ami             = data.aws_ami.ubuntu.id
  size            = "t3.micro"
  subnet_id       = aws_subnet.public_subnets["public_subnet_3"].id
  security_groups = [aws_security_group.vpc-ping.id, aws_security_group.ingress-ssh.id, aws_security_group.vpc-web.id]
}

module "server_subnet_1" {
  source      = "./modules/web_server"
  ami         = data.aws_ami.ubuntu.id
  key_name    = aws_key_pair.generated.key_name
  user        = "ubuntu"
  private_key = tls_private_key.generated.private_key_pem
  subnet_id   = aws_subnet.public_subnets["public_subnet_1"].id
  security_groups = [aws_security_group.vpc-ping.id,
    aws_security_group.ingress-ssh.id,
  aws_security_group.vpc-web.id]
}

module "autoscaling" {
  source = "github.com/terraform-aws-modules/terraform-aws-autoscaling?ref=v4.9.0"

  # Autoscaling group
  name = "myasg"

  vpc_zone_identifier = [aws_subnet.private_subnets["private_subnet_1"].id,
  aws_subnet.private_subnets["private_subnet_2"].id, 
  aws_subnet.private_subnets["private_subnet_3"].id]
  min_size            = 0
  max_size            = 1
  desired_capacity    = 1

  # Launch template
  use_lt    = true
  create_lt = true

  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  tags_as_map = {
    Name = "Web EC2 Server 2"
  }

}

output "public_ip" {
  value = aws_instance.ubuntu_server.public_ip
}

output "public_dns" {
  value = aws_instance.ubuntu_server.public_dns
}

output "public_ip_server_subnet_1" {
  value = aws_instance.web_server.public_ip
}

output "public_dns_server_subnet_1" {
  value = aws_instance.web_server.public_dns
}

output "public_ip_module" {
  value = module.server.public_ip
}

output "public_dns_module" {
  value = module.server.public_dns
}

output "size" {
  value = module.server.size
}

output "asg_group_size" {
  value = module.autoscaling.autoscaling_group_max_size
}

```

## Snippet of Relevant Terraform Code for /workspace/terraform/modules/server/Main.tf
```hcl

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

## Snippet of Relevant Terraform Code for /workspace/terraform/modules/server/Output.tf
```hcl
output "public_ip" {
  description = "IP Address of server built with Server Module"
  value       = aws_instance.web.public_ip
}

output "public_dns" {
  description = "DNS Address of server built with Server Module"
  value       = aws_instance.web.public_dns
}

output "size" {
  description = "Size of server built with Server Module"
  value       = aws_instance.web.instance_type
}
```


## Snippet of Relevant Terraform Code for /workspace/terraform/modules/web_server/server.tf (Before Refactoring)
```hcl
variable "ami" {}
variable "size" {
  default = "t3.micro"
}
variable "subnet_id" {}

variable "user" {}

variable "security_groups" {
  type = list(any)
}

variable "key_name" {

}

variable "private_key" {

}

resource "aws_instance" "web" {
  ami                         = var.ami
  instance_type               = var.size
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = var.security_groups
  associate_public_ip_address = true
  key_name                    = var.key_name
  connection {
    user        = var.user
    private_key = var.private_key
    host        = self.public_ip
  }


  provisioner "remote-exec" {
    inline = [
      "sudo rm -rf /tmp",
      "sudo git clone https://github.com/hashicorp/demo-terraform-101 /tmp",
      "sudo sh /tmp/assets/setup-web.sh",
    ]
  }

  tags = {
    "Name"        = "Web Server from Module"
    "Environment" = "Training"
  }

}

output "public_ip" {
  value = aws_instance.web.public_ip
}

output "public_dns" {
  value = aws_instance.web.public_dns
}
```
