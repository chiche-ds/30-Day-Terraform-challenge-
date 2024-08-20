# Day4: Mastering Basic Infrastructure with Terraform 

## Participant Details
- **Name:** Emmanuel Bernardfomonyuy
- **Task Completed:** 
- **Date and Time:** 

 
# your terraform code 
    ```terraform
        # Your Terraform code here
        provider "aws" {
        region = "us-west-2"
        }

        resource "aws_instance" "example" {
        ami           = "ami-0c55b159cbfafe1f0"
        instance_type = "t2.micro"
        }
    
