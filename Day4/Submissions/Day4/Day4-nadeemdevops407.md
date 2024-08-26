# Day4: Mastering Basic Infrastructure with Terraform

## Participant Details
- **Name:** Nadeem Taj
- **Task Completed:** Deployed both configurable and clustered web servers, reviewed documentation and started creating blog detailing the procedure
- **Date and Time:** 8/21/2024 11:46 PM

 
# Terraform Code - Deploying a Configurable Web Server

I deployed configurable web server using terraform. I have a lot variable in separate file named variable.tf and use these variable in my main.tf file to configured my infrastructure. 


### main.tf

```python
provider "aws" {
  region = var.aws_region
}

resource "aws_security_group" "web_sg" {
  name        = var.security_group_name
  description = "Allow traffic on port ${var.web_port}"

  ingress {
    from_port   = var.web_port
    to_port     = var.web_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow traffic on web port
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # Allow all outbound traffic
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web_instance" {
  ami           = var.ami_id
  instance_type = var.instance_type
  security_groups = [aws_security_group.web_sg.name]

  user_data = <<-EOF
              #!/bin/bash
              apt update
              apt install -y apache2
              echo "Listen ${var.web_port}" >> /etc/apache2/ports.conf
              echo "<VirtualHost *:${var.web_port}>" > /etc/apache2/sites-available/000-default.conf
              echo "    DocumentRoot /var/www/html" >> /etc/apache2/sites-available/000-default.conf
              echo "    <Directory /var/www/html>" >> /etc/apache2/sites-available/000-default.conf
              echo "        AllowOverride All" >> /etc/apache2/sites-available/000-default.conf
              echo "    </Directory>" >> /etc/apache2/sites-available/000-default.conf
              echo "</VirtualHost>" >> /etc/apache2/sites-available/000-default.conf
              systemctl restart apache2
              echo "Hello, World!" > /var/www/html/index.html
              systemctl start apache2
              systemctl enable apache2
              EOF

  tags = {
    Name = var.instance_name
  }
}

output "instance_ip" {
  value = aws_instance.web_instance.public_ip
}
```


### variable files 

```python
variable "aws_region" {
  description = "The AWS region to deploy resources"
  default     = "us-east-1"
}

variable "security_group_name" {
  description = "Name of the security group"
  default     = "web_security_group"
}

variable "web_port" {
  description = "Port for the web server"
  default     = 8080
}

variable "ami_id" {
  description = "AMI ID for the instance"
  default     = "ami-04a81a99f5ec58529"  # Replace with your preferred AMI ID
}

variable "instance_type" {
  description = "Type of instance to deploy"
  default     = "t2.micro"
}

variable "instance_name" {
  description = "Name tag for the instance"
  default     = "configurable-web-server-day4"
}
```