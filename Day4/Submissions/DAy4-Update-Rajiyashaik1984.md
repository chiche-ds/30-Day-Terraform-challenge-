Participant Details
Name: Rajiya Shaik
Task Completed:
Reading: Chapter 2 of "Terraform: Up & Running" by Yevgeniy Brikman.
Pages: 60 - 69.
Udemy Videos:
Watched "Input Variables" (Video 14).
Watched "Local Variables" (Video 15)

 Learnt - How to use input and local variables in Terraform for more flexible and reusable configurations, and hands-on of Deployment of Highly Available Web App on AWS using Terraform.
Date and Time: 30-08-2024



Day-3 deploy a congigurable webserver--main.tf
```
terraform {
    required_providers {
      aws = {
        source = "hashicorp/aws"
        version = "~> 4.16"
      }
    }
    required_version = " 1.9.5"
}
provider "aws" {
    region = "us-east-1"
}

resource "aws_instance" "my_server" {
    ami = "ami-0e86e20dae9224db8"
    instance_type = "t2.micro"
    vpc_security_group_ids = [ aws_security_group.sg1.id ]
    
    tags ={
        Name ="appserver"
    }
user_data = <<-EOF
                #!bin/bash
                echo "Hello world/ This is Razia on 30 day-Terraform-challenge" > index.html
                nohup busybox httpd -f -p ${var.server_port} &
                EOF


   user_data_replace_on_change = true

}
resource "aws_security_group" "sg1" {
    name = "terraform-my_server-instance"
    ingress {
        from_port = var.server_port
        to_port = var.server_port
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

variable "server_port" {
    description = "The port the server will use for HTTP requests"
    type= number
    default = 8080
  
}

```
Day4-Deploy a clustered webserver with the help of Autosacling group using Terraform.

main.tf
```
terraform {
    required_providers {
      aws = {
        source = "hashicorp/aws"
        version = "~> 4.16"
      }
    }
    required_version = " 1.9.5"
}
provider "aws" {
    region = "us-east-1"
}


   
resource "aws_launch_configuration" "example" {
    image_id = "ami-0e86e20dae9224db8"
    instance_type = "t2.micro"
    security_groups =  [ aws_security_group.sg1.id ]
    

    user_data = <<-EOF
                #!bin/bash
                echo "Hello world/ This is Razia on 30 day-Terraform-challenge" > index.html
                nohup busybox httpd -f -p ${var.server_port} &
                EOF

#Required when using a launch configuration with an auto scaling group.
   lifecycle {
    create_before_destroy = true
   }

}
resource "aws_autoscaling_group" "example" {
  launch_configuration = aws_launch_configuration.example.name
  availability_zones = [ "us-east-1a","us-east-1b" ]


  min_size = 2
  max_size = 10
  tag{
    key= "Name" 
    value = "terraform-asg-example"
    propagate_at_launch = true

  }
}
resource "aws_security_group" "sg1" {
    name = "terraform-my_server-instance"
    ingress {
        from_port = var.server_port
        to_port = var.server_port
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

variable "server_port" {
    description = "The port the server will use for HTTP requests"
    type= number
    default = 8080
  
}

```