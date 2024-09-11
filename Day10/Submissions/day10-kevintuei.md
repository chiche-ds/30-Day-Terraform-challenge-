# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** Kevin Tuei
- **Task Completed:** Completed taks on loops with for_each expressions, for expressions, count parameter and for string directive.
- I also learnt how to enforce tagging standards with default_tags
- **Date and Time:** 3/09/2024 10:10PM 

## Terraform Code Snippet showing how to deploy multipl instances with count
```hcl
resource "aws_instance" "web" {
  count         = 3
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  tags = {
    Name = "web-${count.index}"
  }
}
```

