### Let’s experiment with workspaces on some Terraform code that deploys a single EC2 Instance

```hcl
resource "aws_instance" "example" {
ami = "ami-04a81a99f5ec58529"
instance_type = "t2.micro"
}
terraform {
backend "s3" {
# Replace this with your bucket name!
bucket
= "terraform-up-and-running-state"
key = "workspaces-example/terraform.tfstate"
region = "us-east-1"
# Replace this with your DynamoDB table name!
dynamodb_table = "terraform-up-and-running-locks"
encrypt= true
}
}
```