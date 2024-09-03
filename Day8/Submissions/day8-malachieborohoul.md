# Day 8: Reusing Infrastructure with Modules

## Participant Details
- **Name:** BOROHOUL Soguelni Malachie
- **Task Completed:** I understood the purpose of creating modules which is to write reusable, maintenable and testable Terraform code. I refactored my EC2 instance code by creating a common module.
- **Date and Time:** 8/28/2024 11:32 PM


#Refactor EC2 instance code by creating a Module and also adding Module inputs

##modules/services/webserver/main.tf
```hcl
resource "aws_instance" "example" {
  ami                         = "ami-0b0ea68c435eb488d"
  instance_type               = var.instance_type
  vpc_security_group_ids      = [aws_security_group.instance.id]
  user_data                   = <<-EOF
                #!/bin/bash
                   echo "Hello, World" > index.html
                   nohup busybox httpd -f -p ${var.server_port} &
                   EOF
  user_data_replace_on_change = true


  tags = {
    Name = "terraform-example"
  }
}


resource "aws_security_group" "instance" {
  name = var.instance_name

  ingress {

    to_port   = var.server_port
    from_port = var.server_port

  }
}

```

##modules/services/webserver/variables.tf
```hcl
variable "server_port" {
    description = "The port the server will use for HTTP requests"
  type = number
  default = 8080
}


variable "instance_type" {
  description = "The type of EC2 instances "
  type = string
}

variable "asg_name" {
  description = "The name use for the aws_security_group"
  type = string
}

```

#Add a staging EC2 instance with module input added
##stage/services/webserver/main.tf
```hcl
provider "aws" {
  region = "us-east-1"
}


module "webserver" {
  source = "../../../modules/services/webserver"
  instance_type = "t2.micro"
  asg_name = "terraform-example-instance"
}
```

