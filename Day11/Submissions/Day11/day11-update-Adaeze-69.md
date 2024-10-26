# Day 11: Terraform Conditionals

## Participant Details

- **Name:** Adaeze Nnamdi-Udekwe
- **Task Completed:** I learned how to use loops and conditionals in Terraform for dynamic deployments using `for_each` and `count` in arrays. I also watched videos on Udemy on Variable Collection, Structure Types
Working with Data Blocks, and Terraform Built-in Functions
- **Date and Time:** 09-11-24 and 4:18pm

## Terraform Code 

`main.tf` 

```hcl
provider "aws" {
region = "us-east-2"
}

resource "aws_iam_user" "example" {
for_each = toset(var.user_names)
name = each.value
}
```
`variables.tf`

```hcl
variable "user_names" {
description = "Create IAM users with these names"
type = list(string)
default = ["neo", "trinity", "morpheus"]
}
```
`output.tf`
```hcl
output "all_users" {
value = aws_iam_user.example
}
```

