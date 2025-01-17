# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** Jully Achenchi
- **Task Completed:** Completed taks on loops with for_each expressions, for expressions, count parameter
- **Date and Time:** 20/12/2024 

## Terraform Code Snippet showing how to deploy multipl instances with count
```hcl
//create 3 buckets, defined in variables with exact names
//The length function (get the length)
//Array lookup syntax  var.user_names[1]
resource "aws_s3_bucket" "tr-bucket" {
  count = length(var.bucket_names)
  bucket = var.bucket_names[count.index]
}

resource "aws_s3_bucket" "tr-bucket" {
  for_each = toset(var.bucket_names) //toset to convert the var.bucket_names list into a set.
  bucket = each.value
}

```