# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** Utibe Okon (yutee)
- **Task Completed:** 
    - Read chapter 5 (pages 141-160)
    - Used loops and conditionals in terrafrom code
    - Deployed resources conditionally based on input (variable)
- **Date and Time:** Sat 12 October, 2024 | 7:11 PM GMT+1

## Terraform Code 
```hcl
# creating multiple users programmatically
resource "aws_iam_user" "new_user" {
  for_each = toset(var.user_names)
  name     = each.value
}
# variable.tf
variable "user_names" {
  description = "Create IAM users with these names"
  type        = list(string)
  default     = ["kunle", "emeka", "haruna"]
}


# creating a user on aws based on the name provided in the variable
# main.tf
resource "aws_iam_user" "new_user" {
  name = var.user_name
}
# variables.tf
variable "user_name" {
  description = "Username for new user"
  type        = string
}
# outputs.tf
output "user_arn" {
  value       = aws_iam_user.new_user.arn
  description = "The ARN of the created IAM user"
}

# tfvars file
user_name = <name_of_user>
```
