# Day 11: Using conditional with dadta blockes and variables 

## Participant Details

- **Name:sodiane123
- **Task Completed:using conditionals in terraform
- **Date and Time:10/16/24 

## Terraform Code 
```hcl
variable "deploy_prod" {
  description = "Boolean to control deployment in production"
  type        = bool
  default     = false
}

resource "aws_instance" "conditional_ec2" {
  count = var.deploy_prod ? 1 : 0
  ami           = "ami-0742b4e673072066f"
  instance_type = "t2.medium"

  tags = {
    Name = "Production-Instance"
  }
}



```
## Architecture 

[Name](link to image in S3 bucket)
