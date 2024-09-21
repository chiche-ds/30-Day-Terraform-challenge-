## Participant Details

- **Name:** Ngwa Dieudonne Lobuin
- **Task Completed:** : Workspace Layout and File Layouts
- **Date and Time:** 2024-09-19 4:45am

- 
```hcl
variable "environments" {
  type = list(string)
  default = ["dev", "prod"]
}

resource "aws_instance" "web" {
  for_each = { for env in var.environments : env => env if env != "dev" }

  ami           = "ami-12345678"
  instance_type = "t2.micro"
  tags = {
    Name = "web-${each.key}"
  }
}
```
