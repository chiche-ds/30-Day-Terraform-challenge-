# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** Franklin Afolabi
- **Task Completed:** Learn the importance of loops and when it is best to use count, for_each and for anlong with the subtle differences.
- **Date and Time:** Septmeber 19 2330hrs

## Terraform Code 
```hcl

# variable.tf
variable "user_name" {
  description = "Create IAM users with these names"
  type = list(string)
  default = [ "di", "snipes", "drugs" ]
}


# output.tf
output "first_arn" {
    value = aws_iam_user.example[0].arn
    description = "The ARN for the first user"
}

output "all_arn" {
    value = aws_iam_user.example[*].arn
    description = "The ARN for all user"
}

# Module
resource "aws_iam_user" "example" {
    name = var.user_name
}

variable "user_name" {
    description = "The user name to use"
    type = string
}

output "user_arn" {
    value = aws_iam_user.example.arn
    description = "The ARN of the created IAM user"
}

# Using count

resource "aws_iam_user" "example" {
  count = length(var.user_name)
  name = var.user_name[count.index]
}

module "users" {
    source = "../../../modules/landing-zone/iam-user"
    
    count = length(var.user_name)
    user_name = var.user_name[count.index]
}

# Using for_each

resource "aws_iam_user" "example" {
  for_each = toset(var.user_name)
  name = each.value
}

output "all_users" {
    value = aws_iam_user.example
}

output "all_arns" {
    value = values(aws_iam_user.example)[*].arn
}




```
## Architecture 

[Name](link to image in S3 bucket)

