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
