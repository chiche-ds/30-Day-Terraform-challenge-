# Day 2: Deploying Basic Infrastructure with Terraform

## Participant Details
- **Name:** Utibe Okon (yutee)
- **Task Completed:** Deploying Basic Infrastructure with Terraform
- **Date and Time:** 11th Oct 2024 23:40 WAT

`main.tf`
```hcl
provider "aws" {
region = "us-east-2"
}


resource "aws_instance" "webserver" {
    ami = "ami-04a81a99f5ec58529"
    instance_type = "t2.micro"

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

deployed webserver
![screenshot](webserver.png)