# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** Eddie Chem
- **Task Completed:** Learned how the Terraform arguments `count` and `for_each` are used to create multiple resources or modules based on a set of values, and how they are used in slightly different ways depending on the use case.
- **Date and Time:** 9/03/2024 1:52 PM

## Terraform Code: 
This configuration creates a single IAM user in AWS. `The aws_iam_user` resource is used, and the username is provided through a variable called `user_name`. The ARN (Amazon Resource Name) of the created user is outputted, allowing you to reference this user elsewhere in your Terraform code.
## Creating a Single IAM User
```hcl
# main.tf
resource "aws_iam_user" "example" {
  name = var.user_name
}
# variables.tf
variable "user_name" {
  description = "The user name to use"
  type        = string
}
# outputs.tf
output "user_arn" {
  value       = aws_iam_user.example.arn
  description = "The ARN of the created IAM user"
}
```
## Creating 3 IAM Users with `for_each` Argument Loops
In this setup, three IAM users are created using the `for_each` argument, which loops over a set of usernames provided in the `user_names` variable. Each user is created with the name from the set, and the ARNs of all created users are outputted. Additionally, the entire user resource is outputted for further reference.
## (Directory: modules/landing-zone/iam-user)
```hcl
# main.tf
resource "aws_iam_user" "example" {
  for_each = toset(var.user_names)
  name     = each.value
}
# variables.tf
variable "user_names" {
  description = "Create IAM users with these names"
  type        = list(string)
  default     = ["ed", "edd", "eddie"]
}
# outputs.tf
output "all_arns" {
  value = values(aws_iam_user.example)[*].arn
}

output "all_users" {
  value = aws_iam_user.example
}
```
## Creating 3 IAM Users with Iterative Count Arguments
This example demonstrates how to create multiple IAM users using the count argument to iterate over a list of usernames. The module block is used to call a module that creates users, iterating through each name in the `user_names` list. The ARNs of all the created users are outputted, similar to the previous example.
## (Directory: live/global/iam) 
```hcl
# main.tf
module "users" {
  source = "../../../modules/landing-zone/iam-user"

  count     = length(var.user_names)
  user_name = var.user_names[count.index]
}
# variables.tf
variable "user_names" {
  description = "Create IAM users with these names"
  type        = list(string)
  default     = ["ed", "edd", "eddie"]
}
# outputs.tf
output "user_arns" {
  value       = module.users[*].user_arn
  description = "The ARNs of the created IAM users"
}
```


