## Participant Details
- **Name:** Jully Achenchi
- **Task Completed:** Deploying a web server on AWS
- **Date and Time:** 10/12/2024

### Terraform code
**providers.tf**
```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~>5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  profile = "devops-admin"
}
```

**web-network.tf**
```hcl
resource "aws_vpc" "my-vpc" {
    cidr_block = "10.0.0.0/16"

    tags = {
      Name = "Project1-vpc"
    }
  
}

resource "aws_subnet" "public-subnet" {
    vpc_id = aws_vpc.my-vpc.id
    cidr_block = "10.0.0.0/24"
    availability_zone = "us-east-1a"
    map_public_ip_on_launch = true

    tags = {
      Name = "Project1-subnet"
    }
}

resource "aws_internet_gateway" "webserver-igw" {
  vpc_id = aws_vpc.my-vpc.id

  tags = {
    Name = "Project1-IGW"
  }
}

resource "aws_route_table" "webserver-rt" {
  vpc_id = aws_vpc.my-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.webserver-igw.id
  }

  tags = {
    Name = "public Route table"
  }
}

resource "aws_route_table_association" "public-subnet-asso" {
    subnet_id = aws_subnet.public-subnet.id
    route_table_id = aws_route_table.webserver-rt.id

  
}

resource "aws_security_group" "webserver-sg" {
  name = "web-sg"
  description = "Enable ssh and http connection on port 80 and port 22"
  vpc_id = aws_vpc.my-vpc.id

  ingress {
    description = "http access"
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "ssh access"
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  
  egress {
    from_port = 0
    to_port = 0
    protocol = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Project1-sg"
  }
}
```

**Variables.tf**
```hcl
variable "aws_region" {
  default = "us-east-1"
}

variable "instance_name" {
    description = "This is the name of your instance"
    default = "Website-instance"  
}

variable "instance_type" {
    default = "t2.micro"
}

variable "key_name" {
  default = "Project1"
}
```
**ec2.tf**
```hcl
## AMI Lookup
data "aws_ami" "amazon-ami" {
  most_recent = true
  owners = ["amazon"]

  filter {
    name = "owner-alias"
    values = ["amazon"]
  }

  filter {
    name = "name"
    values = ["amzn2-ami-hvm*"]
  }
}

## Launch an EC2 instance to install your webserver
resource "aws_instance" "web-server" {
  ami = data.aws_ami.amazon-ami.id
  instance_type = var.instance_type
  subnet_id = aws_subnet.public-subnet.id
  key_name = var.key_name
  vpc_security_group_ids = [aws_security_group.webserver-sg.id]
  user_data = file("userdata.sh")

  tags = {
    Name = var.instance_name
  }
}


resource "aws_s3_bucket" "tf-state-bucket" {
  bucket = "terraform-state-jully"
  force_destroy = true
  /*lifecycle {
    prevent_destroy = true
  }*/
}

resource "aws_s3_bucket_versioning" "tf-state-bucket-versioning" {
  bucket = aws_s3_bucket.tf-state-bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "tf-state-bucket-encryption" {
  bucket = aws_s3_bucket.tf-state-bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "tf-state-bucket-public-access-block" {
  bucket = aws_s3_bucket.tf-state-bucket.id

  block_public_acls       = true
  block_public_policy     = true
  restrict_public_buckets = true
  ignore_public_acls      = true
}

resource "aws_dynamodb_table" "tf_state-lock" {
  name         = "terraform-state-lock"
  hash_key     = "LockID"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```
**userdata.sh**
```sh
#!/bin/bash
sudo yum update -y
sudo yum install -y httpd
sudo systemctl enable httpd
sudo systemctl start httpd
echo "<html><body><h1>Hello from the internet</h1></body></html>" > var/www/html/index.html
```