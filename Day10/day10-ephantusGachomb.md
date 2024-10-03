# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** Ephantus Gachomba
- **Task Completed:** Completed taks on loops with for_each expressions, for expressions, count parameter
- **Date and Time:** 12/09/2024 8:00PM 

## Terraform Code Snippet showing how to deploy multipl instances with count
```hcl
//create 3 users, defined in variables with exact names
//The length function (get the lenght)
//Array lookup syntax  var.user_names[1]
resource "aws_iam_user" "example" {
  count = length(var.user_names)
  name = var.user_names[count.index]
}

resource "aws_iam_user" "example" {
  for_each = toset(var.user_names) //toset to convert the var.user_names list into a set.
  name = each.value
}


```
