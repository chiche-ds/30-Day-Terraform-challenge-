##Day 13:Managing Sensitive Data in Terraform

//main.tf
 #Provider block
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

#EC2 instance
resource "aws_instance" "web_server" {
  ami           = "ami-04505e74c0741db8d"
  instance_type = "t2.micro"

  #Attaching the instance profile
  iam_instance_profile = aws_iam_instance_profile.instance.name 
}

#IAM policy document
data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

#IAM role
resource "aws_iam_role" "admin" {
  name_prefix        = var.name
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

#IAM policy document defining an EC2 admin permissions
data "aws_iam_policy_document" "ec2_admin_permissions" {
  statement {
    effect    = "Allow"
    actions   = ["ec2:*"]
    resources = ["*"]
  }
}

#Attaching IAM role policy to IAM role
resource "aws_iam_role_policy" "admin_role_policy" {
  role   = aws_iam_role.admin.name 
  policy = data.aws_iam_policy_document.ec2_admin_permissions.json
}

#IAM instance profile for EC2 instance
resource "aws_iam_instance_profile" "instance" {
  role = aws_iam_role.admin.name 
}


//variable.tf
variable "name" {
  description = "This represents the prefix for the role name"
  type        = string
}
