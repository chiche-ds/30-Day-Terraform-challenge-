## Participant Details
- **Name:** gus
- **Task Completed:** 
- **Date and Time:** 9/5/2024 20:30 PM

 
# Create a basic Terraform module for a common infrastructure component (EC2 instance, S3).
```hcl
# Terraform configuration
provider "aws" {
  region = "us-west-1"
  profile = "Admin"
}

# Create EC2 instance
module "ec2_instances" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 4.3.0" # Use the latest version
  count   = 1

  name = "my-terraform-ec2-instance"

  ami           = "ami-0e64c0b934d72ced5"
  instance_type = "t2.micro"

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}

# This configuration creates a public S3 bucket with a variable
resource "aws_s3_bucket" "my-terraform-bucket" {
  
  tags = {
    Terraform   = "true"
    Environment = "dev"
    Name = var.my-terraform-bucket
  }
}



```

## Creating infrastructure using a reuseable module

```hcl
module "aws-s3-static-website-bucket" {
  source = "./modules/aws-s3-static-website-bucket"

  bucket_name = "Terraform-module-bucket.id"

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}
```
