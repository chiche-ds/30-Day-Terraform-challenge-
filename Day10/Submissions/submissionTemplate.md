# Day 10: Title here 

## Participant Details

- **Name:sodiane123
- **Task Completed:**Loops in Terraform
- **Date and Time:10/16/24

## Terraform Code 
```hcl
variable "instance_details" {
  description = "List of maps containing instance configurations"
  type = map(object({
    ami           = string
    instance_type = string
  }))
  default = {
    instance1 = { ami = "ami-0c55b159cbfafe1f0", instance_type = "t2.micro" }
    instance2 = { ami = "ami-00b6a8a2bd28daf19", instance_type = "t2.small" }
    instance3 = { ami = "ami-0742b4e673072066f", instance_type = "t2.medium" }
  }
}

resource "aws_instance" "ec2" {
  for_each      = var.instance_details
  ami           = each.value.ami
  instance_type = each.value.instance_type

  tags = {
    Name = each.key
  }
}



```
## Architecture 

[Name](link to image in S3 bucket)

