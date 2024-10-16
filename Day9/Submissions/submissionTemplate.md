# Day 9: Continue reUse of infrastructure with terraform modules

## Participant Details

- **Name:Solang Ngemnyi 
- **Task Completed:Continued reading chap.4 terraform modules 
- **Date and Time:10/16/24

## Terraform Code 
```hcl
variable "environment" {
  description = "The environment to deploy (dev, staging, production)"
  type        = string
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = map(string)  # Map to support multiple environments
  default = {
    dev     = "ami-0c55b159cbfafe1f0"     # Replace with a dev AMI ID
    staging = "ami-00b6a8a2bd28daf19"     # Replace with a staging AMI ID
    prod    = "ami-0742b4e673072066f"     # Replace with a prod AMI ID
  }
}

variable "instance_type" {
  description = "Instance type for the EC2 instance"
  type        = map(string)  # Map to support multiple environments
  default = {
    dev     = "t2.micro"
    staging = "t2.small"
    prod    = "t2.medium"
  }
}



```
## Architecture 
[Name](link to image in S3 bucket)

