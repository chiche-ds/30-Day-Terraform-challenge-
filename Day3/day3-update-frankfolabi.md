# Day 3: Deploying Basic Infrastructure With Terraform

## Participant Details

- **Name:** Franklin Afolabi
- **Task Completed:** Tasks for Day 3 completed. Read the 2 sections in the book and watched the recommended videos on Plug-in architecture, Provider Block and resource block.
- **Date and Time:** August 24, 2024 0530

## Embedded Terraform Code 

main.tf
// This is the provider block showing the region to be used
provider "aws" {
    region = "us-east-2"
}

// Create the resource block for the webserver and attach the securiity group 
// Create a user data script the fires up when the server is launched
resource "aws_instance" "webserver" {
    ami = "ami-0fb653ca2d3203ac1"
    instance_type = "t2.micro"
    vpc_security_group_ids = [aws_security_group.instance.id]

    user_data = <<-EOF
    #!/bin/bash
    echo "Hello, World. Welcome to the use of Terraform in deploying infrastructure" > index.html
    nohup busybox httpd -f -p 8080 &
    EOF

    user_data_replace_on_change = true

    tags = {
        Name = "tf-webserver"
    }
}


// Create the security group to allow port 8080 from any IPv4 address
resource "aws_security_group" "instance" {
    name = "tf-sg"

    ingress {
        from_port = 8080
        to_port = 8080
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    } 
}