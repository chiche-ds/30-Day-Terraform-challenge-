# Day 11: Terraform Conditionals

## Participant Details

- **Name:** Otu Michael Udo
- **Task Completed:** I learned how to use loops and conditionals in Terraform for dynamic deployments using `for_each` and `count` in arrays.
- **Date and Time:** 12-17-24 and 4:35pm

## Terraform Code 
variable "environment" {
  description = "The environment to deploy (dev or prod)"
  type        = string
  default     = "prod"
}

locals {
  #If the environment is prod, it uses a larger instance (t3.large)  
  instance_type = var.environment == "prod" ? "t3.large" : "t2.micro"  
}

resource "aws_instance" "smart_instance" {
  ami           = "ami-0e2c8caa4b6378d8c"  #ubuntu ami
  instance_type = local.instance_type
  subnet_id     = "subnet-03a4e65b08e499754"

  tags = {
    Name        = "conditional-instance" #Gives the name of the instance
    Environment = var.environment #Tags the instance with the selected environment (dev or prod).
  }
}