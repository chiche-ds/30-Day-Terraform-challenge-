## Author: Joel Ebenka

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.63.0"
    }
  }
}

# Create default VPC if one does not exist
resource "aws_default_vpc" "default_vpc" {}

# Use data source to get all availability zones in the region
data "aws_availability_zones" "available_zones" {}

# Create default subnet if one does not exist
resource "aws_default_subnet" "default_az1" {
  availability_zone = data.aws_availability_zones.available_zones.names[0]
  tags = {
    Name = "30_days_server"
  }
}
