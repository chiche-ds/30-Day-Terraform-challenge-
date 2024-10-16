# Day 12: Zero Downtime Deployment

## Participant Details

- **Name:** William Maina
- **Task Completed:** Zero Downtime deployment using terraform
- **Date and Time:** 16-10-2024


## Terraform Code 
Achieving zero downtime deployment using terraform `create before destroy` lifecycle on EC2 instances to be specific. It ensures your state file is consistent and avoids conflicts
```hcl
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  key_name      = "my-key-pair"
  
  tags = {
//adds a new unique name to avoid conflict with the old instance
    Name = "web-server-${terraform.timestamp()}"
  }

//Provisions a new EC2 instance before deleting the old one.
  lifecycle {
    create_before_destroy = true
  }
}


```
