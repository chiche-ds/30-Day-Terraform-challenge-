# Day 11: Terraform Conditionals

## Participant Details

- **Name:** EJIBODE IBRAHEEM A
- **Task Completed:** Solidified my understanding of terraform conditionals.
- **Date and Time:** 14/12/2024 12:50 PM

There are several wasy to acheive conditional provisioning with terraform, they include:

- `count parameter` | Used for conditional resources
- `for_each and for expressions` | Used for conditional resources and inline blocks within a resource
- `if string directive` | Used for conditionals within a string

## Terraform Code 
```hcl
    count = var.enable_autoscaling ? 1 : 0

# if else acheived by combining foreach and the tenary operator
resource "aws_iam_user_policy_attachment" "neo_cloudwatch_full_access" {
    count = var.give_neo_cloudwatch_full_access ? 1 : 0
    user = aws_iam_user.example[0].name
    policy_arn = aws_iam_policy.cloudwatch_full_access.arn
}

resource "aws_iam_user_policy_attachment" "neo_cloudwatch_read_only" {
    count = var.give_neo_cloudwatch_full_access ? 0 : 1
    user = aws_iam_user.example[0].name
    policy_arn = aws_iam_policy.cloudwatch_read_only.arn
}

```