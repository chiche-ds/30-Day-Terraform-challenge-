# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** Alvin Ndungu
- **Task Completed:** Terraform Loops and Conditionals
- **Date and Time:** 2024-08-20 15:18pm



- count parameter, to loop over resources and modules
- for_each expressions, to loop over resources, inline blocks within a resource, and modules
- for expressions, to loop over lists and maps
- for string directive, to loop over lists and maps within a string

```
resource "aws_iam_user" "example" {
count = 3
name = "neo.${count.index}"
}
```


`for` expressions are used to transform or filter collections (lists, maps) within resource properties or variables.

#### List Example:

```
variable "zones" {
  type = list(string)
  default = ["us-west-1a", "us-west-1b", "us-west-1c"]
}

output "zone_names" {
  value = [for zone in var.zones : "${zone} is available"]
}

