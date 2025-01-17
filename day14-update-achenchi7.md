# Day 14: Working with Multiple Providers

## Participant Details

- **Name:** Jully Achenchi
- **Task Completed:** Working with Multiple Providers
- **Date and Time:** 29/12/2024

## Working with Multiple Providers

(add an alias to each provider:)

### deploying 2 EC2 Instances in different regions in aws
```hcl
## region  1 
provider "aws" {
  region = "us-east-2"
  alias = "region_1"
}
## region  2
provider "aws" {
  region = "us-west-1"
  alias = "region_2"
}

#deploy 2 EC2 Instances in different regions
resource "aws_instance" "region_1" {
  provider = aws.region_1
  ami = data.aws_ami.ubuntu_region_1.id
  instance_type = "t2.micro"
}

resource "aws_instance" "region_2" {
  provider = aws.region_2
  ami = data.aws_ami.ubuntu_region_2.id
  instance_type = "t2.micro"
}

```
