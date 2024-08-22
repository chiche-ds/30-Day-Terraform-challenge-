variable "aws_region" {
  description = "The AWS region to deploy resources in"
  default     = "us-east-1"
  type        = string
}

variable "profile" {
  description = "The AWS CLI profile to use"
  default     = "default"
  type        = string
}

variable "aws_instance_type" {
  description = "The type of AWS EC2 instance"
  default     = "t2.micro"
  type        = string
}

variable "aws_key_pair" {
  description = "The name of the AWS key pair"
  default     = "my_ec2_key"
  type        = string
}
