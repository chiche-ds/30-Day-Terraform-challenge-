


## terraform/modules/provider/main.tf
```hcl
provider "aws" {
  region = var.region
}
```

## terraform/modules/provider/variables.tf
```hcl
variable "region" {
  description = "The AWS region to deploy resources"
}
```

## terraform/modules/ec2-instance/main.tf
```hcl
data "aws_ami" "latest" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["amazon"]
}

resource "aws_instance" "this" {
  ami           = data.aws_ami.latest.id
  instance_type = var.instance_type
  tags = {
    Name = "production-instance"
  }
}
```

## terraform/modules/ec2-instance/variables.tf
```hcl
variable "instance_type" {
  description = "The EC2 instance type"
}
```

## terraform/modules/ec2-instance/outputs.tf
```hcl
output "instance_id" {output "instance_id" {
  description = "The ID of the EC2 instance"
  value       = aws_instance.this.id
}
```
