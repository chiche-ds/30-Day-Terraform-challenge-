## Participant Details
- **Name:** William Maina
- **Task Completed:** :  loops and conditionals.
- **Date and Time:** 2024-10-13 08:00pm
- 
# Task Completed

Use count to deploy multiple instances of the same resource, and use for_each to iterate over maps or lists of resources.
Implement conditional logic to deploy resources based on input variables.

### Create three separate IAM users 
main.tf
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_user" "example" {
  for_each = toset(var.user_names)
  name = each.value
}
```
variables.tf
```
variable "user_names" {
  description = "create 3 iam users"
  type = list(string)
  default = [ "Neo", "Trinity", "morpheus" ]
}
```
output.tf
```
output "all_users" {
  value = aws_iam_user.example
}
```
### Create 3 different EC2 instances using terraform modules
```
module "ec2-instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "5.7.1"

  name = "VmInstances-${count.index}"
  count = 3

  ami = "ami-2893nkfn483k2"
  instance_type = "t3.micro"

  tags = {
    terraform = true
    Environment= "dev"
  }
}
