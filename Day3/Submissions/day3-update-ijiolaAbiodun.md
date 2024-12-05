provider "aws" {
    region = us-east-1
  
}

resource "aws_instance" "single_server" {
    ami = "ami-0fb653ca2d3203ac1"
    instance_type = "t2.micro"
  
}

resource "aws_instance" "terraform_web_server_instance" {
    ami =  "ami-0fb653ca2d3203ac1" 
    instance_type = "t2.micro"
    vpc_security_group_ids = [aws_security_group.instance.id]

    user_data = <<-EOF
     #!/bin/bash
    echo "Hello, World" > index.html
    nohup busybox httpd -f -p 8080 &
    EOF
user_data_replace_on_change = true

tags = {
  Name = "terraform_web_server_instance"
}
}

resource "aws_security_group" "terraform_web_server_instance" {
    name = "terraform_web_server_instance"

    ingress = {
        from_port = 8080
        to_port = 8080
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
  
}


