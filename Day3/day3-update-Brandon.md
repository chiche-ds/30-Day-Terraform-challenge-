# Day 3: Deploying Basic Infrastructure With Terraform

## Participant Details

- **Name:** Meh Brandon
- **Task Completed:** Read the Book, watched the videos and deployed a single web server using AWS
- **Date and Time:** 08-26-2024 at 11:25 pm

## Terraform Code 

The provided Terraform code sets up an AWS EC2 instance in the `us-east-1` region using an Ubuntu Amazon Machine Image (AMI). It configures the instance as a small, low-cost server (`t2.micro`) and runs a simple web server that displays "Hello, World" on port 8080. A security group is also created to allow incoming traffic on port 8080 from any IP address, ensuring that the web server is accessible over the internet.The terraform user_data_replace on change parameter is to true so that when you change the user_data parameter and run apply, terraform will terminate any original instance and launch a totally new one. I also learned that when you create a security group, you haveto attachitto your instanceand terraform takes care of which resouces will be created first.

provider  "aws" {
    region = "us-east-1"
}

resource "aws_instance" "My-Ec2instance" {
 ami = "ami-0e86e20dae9224db8"
 instance_type = "t2.micro"
 vpc_security_group_ids = [aws_security_group.instance.id]


 user_data = <<-EOF
             #!/bin/bash
             echo "Hello, World" > index.html
             nohup busybox httpd -f -p 8080 &
                 

                  EOF
             user_data_replace_on_change = true
 tags = {
    Name = "Terraform-Instance"
 }
}

resource "aws_security_group" "instance" {
 name = "terraform-SG-instance"
 ingress {
 from_port = 8080
 to_port = 8080
 protocol = "tcp"
 cidr_blocks = ["0.0.0.0/0"]
 }
}