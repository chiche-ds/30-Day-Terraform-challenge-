# Day 3: Deploying Basic Infrastructure with Terraform

## Participant Details

- **Name:** Ebenka christian joel
- **Task Completed:** "Setting Up Your AWS Account", "Installing Terraform", and "Configuring VS Code"
                        ""Terraform Plug-in Based Architecture" (Video 11)
- **Date and Time:** 22-08-2024 at 17:32 pm


## Terraform code : Created a terraform folder containing the code to deploy a simple http-server on an ec2 machine

1-main.tf:

```bash
##Author: Joel Ebenka

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.63.0"
    }
  }
}

Create default VPC if one does not exist
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


```


2-Ec2.tf:

```bash
##Author: Joel Ebenka 
resource "aws_security_group" "web_ec2_security_group" {
  name        = "ec2_web_server_security_group"
  description = "allow access on ports 8080 and 22"
  vpc_id      = aws_default_vpc.default_vpc.id

  ingress {
    description = "http proxy access"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "ssh access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "server_security_group"
  }
}

data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "owner-alias"
    values = ["amazon"]
  }

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm*"]
  }
}

resource "aws_instance" "ec2_instance" {
  ami                    = data.aws_ami.amazon_linux_2.id
  instance_type          = var.aws_instance_type
  subnet_id              = aws_default_subnet.default_az1.id
  vpc_security_group_ids = [aws_security_group.web_ec2_security_group.id]
  key_name               = var.aws_key_pair
  user_data              = <<-EOF
  #!/bin/bash
  sudo yum update -y
  sudo yum install httpd -y
  sudo systemctl start httpd
  sudo systemctl enable httpd
  sudo systemctl status httpd
  echo "<h1> Terraform 30 days challenge day3 Ebenka Joel - Hostname: $(hostname) </h1>" | sudo tee -a /var/www/html/index.html
  EOF
````
  root_block_device {
    volume_size = 30
  }

  ebs_block_device {
    device_name = "/dev/xvdf"
    volume_size = 30
    volume_type = "gp2"
  }

  tags = {
    Name = "ec2_web_server"
  }
}

resource "null_resource" "name" {
  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file(local_file.ssh_key.filename)
    host        = aws_instance.ec2_instance.public_ip
  }

  depends_on = [aws_instance.ec2_instance]
}


```



3-output.tf:

```bash
# print the url of the webserver
output "ec2_web_url" {
  value     = join ("", ["http://", aws_instance.ec2_instance.public_dns, ":", "80"])
}

# print the url of the webserver
output "ssh_connection_command" {
  value     = join ("", ["ssh -i my_ec2_key.pem ec2-user@", aws_instance.ec2_instance.public_dns])
}


