# Day 11: Understanding Terraform Conditionals

## Participant Details
- **Name:** Dwayne Chima
- **Task Completed:** : Use conditionals to deploy resources in a specific environment 
- **Date and Time:** 11th Dec 2024 11:00am

### example code

**main.tf**
```
module "compute" {
  source = "../modules/compute"
  distro_version = "22.04"
  security_group_id = module.network.security_group_id
  subnet_id = module.network.subnet_ids
  environment = var.environment
}
```
**vars.tf**
```
variable "environment" {
  description = "The deployment environment (must be 'dev' or 'prod', in lowercase)"
  type        = string

  # Validate input to ensure it's 'dev' or 'prod' in lowercase
  validation {
    condition     = lower(var.environment) == var.environment && contains(["dev", "prod"], var.environment)
    error_message = "The environment must be either 'dev' or 'prod' and must be in lowercase."
  }
}
```

**module.compute - vars.tf**
```
variable "environment"{}

variable "distro_version" {
  description = "The version of the Linux distribution"
  type        = string
  default     = "24.04" 
}

variable "security_group_id" {
}

variable "subnet_id" {
}

variable "instance_count" {
  description = "number of instances"
  type = number
  default = 1
}

variable "instance_type" {
  default = "t2.micro"
}
```

**module.compue - main.tf**
```
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd*/ubuntu-*-${var.distro_version}-amd64-server-*"]
  }

  owners = ["099720109477"]  # Ubuntu's official AWS account ID
}

resource "aws_instance" "app_instance" {
  count = var.instance_count  # Number of instances to create

  # Use t2.micro for dev and t2.medium for prod based on the environment
  instance_type          = var.environment == "dev" ? "t2.micro" : "t2.medium"
  ami                   = data.aws_ami.ubuntu.id
  subnet_id             = var.subnet_id[count.index % length(var.subnet_id)]
  vpc_security_group_ids = [var.security_group_id]
  key_name = var.private_key.id

  user_data = <<-EOT
    #!/bin/bash
    sudo apt update -y
  EOT
}
```
