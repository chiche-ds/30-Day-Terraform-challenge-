### Submission details 
Name: Nadeem Taj
Date and Time: 19 Aug 2024 at 11:40pm
Blog link: https://medium.com/@nadeemtaj407/49a75455dee6 


### Terraform Code 
```python
provider "aws" {
  region = "us-east-1"  # Change to your preferred region
}

resource "aws_security_group" "web_sg" {
  name        = "web_security_group"
  description = "Allow traffic on ports 22 and 8080"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow SSH from everywhere
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow traffic on port 8080
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # Allow all outbound traffic
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web_instance" {
  ami           = "ami-04a81a99f5ec58529" # Ubuntu AMI ID, copied from AWS console
  instance_type = "t2.micro"
  security_groups = [aws_security_group.web_sg.name]

  user_data = <<-EOF
              #!/bin/bash
              apt update
              apt install -y apache2
              echo "Hello, World!" > /var/www/html/index.html
              systemctl start apache2
              systemctl enable apache2
              EOF

  tags = {
    Name = "web-server-day3"
  }
}

output "instance_ip" {
  value = aws_instance.web_instance.public_ip
}
```