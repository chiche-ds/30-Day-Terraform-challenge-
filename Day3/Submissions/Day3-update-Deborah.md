provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "example" {
  ami           = "ami-0866a3c8686eaeeba"  # Amazon Linux 2 AMI (change for your region) 
  instance_type = "t2.micro"
}