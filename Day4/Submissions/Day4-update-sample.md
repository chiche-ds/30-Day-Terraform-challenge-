# Day4: Day title 

## Participant Details
- **Name:** 
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
    
