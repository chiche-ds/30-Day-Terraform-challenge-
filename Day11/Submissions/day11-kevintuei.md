# Day 11: Terraform Conditionals

## Participant Details

- **Name:** Kevin Tuei
- **Task Completed:** Understood Terraform conditionals and included it on my blog on loops
- **Date and Time:** 4/09/2024

## Conditional Resource Deployment with count

The S3 bucket will only be deployed if the create_bucket variable is set to true.

```hcl
variable "create_bucket" {
  type    = bool
  default = true
}

resource "aws_s3_bucket" "example" {
  count  = var.create_bucket ? 1 : 0
  bucket = "conditional-bucket"
}
```

## Deploying Resources Based on Environment with for_each

Terraform deploys an EC2 instance for each environment but skips the dev environment.

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
