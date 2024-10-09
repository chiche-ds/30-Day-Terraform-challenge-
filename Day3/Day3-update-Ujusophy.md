# Day 3: Deploying Basic Infrastructure with Terraform

## Participant Details

- **Name:** Njoku Ujunwa Sophia
- **Task Completed:** Deploying Basic Infrastructure with Terraform
- **Date and Time:** 2024-08-29 08:54 AM GMT

### main.tf

```
provider "aws" {
    region = "us-east-1"
}

resource "aws_instance" "web_server"{
    ami = "ami-023508951a94f0c71"
    subnet_id = "subnet-0846e4641e585a3df"
    instance_type = "t2.micro"
    security_group = ["sg-0f76c24f265fa8fbd"]
    tags = {
        first = "web_server"
    }
}
```
