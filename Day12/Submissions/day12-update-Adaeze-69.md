# Day 12: Zero-Downtime Deployment with Terraform
## Participant Details

- **Name:** Adaeze Nnamdi-Udekwe
- **Task Completed:** Use Terraform to deploy infrastructure updates with zero downtime using techniques like blue/green deployments. 
- **Date and Time:** 09-14-24 12:44 am

## Terraform Code 
`main.tf`

```hcl
provider "aws" {
  region = "us-east-2"
}



resource "aws_launch_configuration" "example" {
  image_id        = var.ami
  instance_type   = var.instance_type
  security_groups = [aws_security_group.instance.id]
  user_data = templatefile("${path.module}/user-data.sh", {
    server_port = var.server_port
    # db_address  = data.terraform_remote_state.db.outputs.address
    # db_port     = data.terraform_remote_state.db.outputs.port
    server_text = var.server_text
  })

  # Required when using a launch configuration with an auto scaling group.
  lifecycle {
    create_before_destroy = true
  }
}
```

`terraform.tfvars`
```hcl

ami           = "ami-0c55b159cbfafe1f0"
instance_type = "t2.micro"
server_port   = 8080
server_text   = "Hello, World"

```

`variable.tf`

```hcl
variable "ami" {
  description = "The AMI ID to use for the instance"
  type        = string

}

variable "instance_type" {
  description = "The instance type to use for the instance"
  type        = string
}

variable "server_port" {
  description = "The port on which the server will run"
  type        = number
}

variable "server_text" {
  description = "The text to display on the server"
  type        = string
}
```

