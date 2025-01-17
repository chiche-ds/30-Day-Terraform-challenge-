# Day 9: Continue reuse of infrastructure with terraform modules

## Participant Details

- **Name:Yusuf Abdulganiyu 
- **Task Completed:
  Reading: Chapter: Continue with Chapter 4 (Pages 115-139)
            Sections: "Moudel Gotchas ", "Module Versioning".
  Videos: Udemy: Watch the following videos:
      Video 40: "Terraform module - Scope"
      Video 41: "Terraform module - Public registry "
      Video 42: "Terraform module - Versioning"
  Bonus Hands-On Project.
  Blog Post
      - https://medium.com/@abdulganiyu/terraform-modules-demystified-unlocking-versioning-nesting-and-reusability-4d2fd21b2315
  
  Social Media Post
        - https://www.linkedin.com/posts/yusuf-abdulganiyu_terraform-modules-demystified-unlocking-activity-7272012609539776512-tt6r?utm_source=share&utm_medium=member_android


- **Date and Time:12/09/24

## Terraform Code 
```hcl
variable "environment" {  
  description = "Deployment environment"  
  type        = string
  validation = {
      condition = can(regex("^(prod|dev|staging)", var.environment))
      error_message = "Environment must start with 'prod" or 'dev'."
}
}  

resource "aws_s3_bucket" "example" {  
  bucket = "${var.environment}-example-bucket"  
  tags   = { Environment = var.environment }  
}  


variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = map(string)  # Map to support multiple environments
  default = {}
}

variable "instance_type" {
  description = "Instance type for the EC2 instance"
  type        = map(string)  # Map to support multiple environments
  default = {}
}

```
