### Name: Adaeze Nnamdi-Udekwe
### Task: Day 3: Deploying Basic Infrastructure with Terraform
### Date: 8/20/24
### Time: 12:08am

### Deployment of a webserver on a single server

`main.tf` file carrying my aws provider, AWS EC2 instance reosurce block and security group resource block.

```
provider "aws" {
region = "us-east-1"
}


resource "aws_instance" "example" {
ami = "ami-04a81a99f5ec58529"
instance_type = "t2.micro"
vpc_security_group_ids = [aws_security_group.instance.id]
user_data = <<-EOF
#!/bin/bash
echo "Hello, World" > index.html
nohup busybox httpd -f -p 8080 & 
EOF
user_data_replace_on_change = true

tags = {
  Name = "web-server"
}
}

resource "aws_security_group" "instance" {
name = "terraform-example-instance"
ingress {
from_port = 8080
to_port = 8080
protocol = "tcp"
cidr_blocks = ["0.0.0.0/0"]
}
}
```

`terrafrom.tf` file containing the latest version of terraform configurartion.

```
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.63.0"
    }
  }
}



```

webserver showing on my browser.
![web server](image.png)