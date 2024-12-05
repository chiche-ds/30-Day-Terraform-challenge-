# Day 4: Mastering Basic Infrastructure with Terraform

## Participant Details

- **Name:** Ejibode Ibraheem
- **Task Completed:** Deploying Basic Infrastructure with Terraform
- **Date and Time:** 04-12-2024 at 11:44pm

## Terraform Code 



```
provider "aws" {
  region ="us-east-2"
}

resource "aws_instance" "my_instance" {
    ami ="ami-0fb653ca2d3203ac1"
    instance_type = "t2.micro"
    vpc_security_group_ids = [aws_security_group.instance.id]
    user_data = <<-EOF
 #!/bin/bash
 echo "Hello, World" > index.html
 nohup busybox httpd -f -p 8080 &
 EOF
 user_data_replace_on_change = true
    
    tags = {
      Name = "terraform-example"
    }
  
}

variable "server_port" {
 description = "The port the server will use for HTTP requests"
 type = number
 default= 8080
}

resource "aws_security_group" "instance" {
 name = "terraform-example-instance"
 ingress {
 from_port = var.server_port
 to_port = var.server_port
 protocol = "tcp"
 cidr_blocks = ["0.0.0.0/0"]
 }
}


resource "aws_launch_configuration" "example" {
 image_id = "ami-0fb653ca2d3203ac1"
 instance_type = "t2.micro"
 security_groups = [aws_security_group.instance.id]
 user_data = <<-EOF

 #!/bin/bash
 echo "Hello, World" > index.html
 nohup busybox httpd -f -p ${var.server_port} &
 EOF
 lifecycle {
 create_before_destroy = true
 }
}

output "public_ip" {
 value = aws_instance.my_instance.public_ip
 description = "The public IP address of the web server"
}

resource "aws_autoscaling_group" "example" {
 launch_configuration = aws_launch_configuration.example.name
 min_size = 2
 max_size = 10
 tag {
 key = "Name"
 value = "terraform-asg-example"
 propagate_at_launch = true
 }
}

```