# Day4: Day title 

## Participant Details
- **Name:** bennyfmo
- **Task Completed:** Deploying a Configurable webserver
- **Date and Time:** 20/08/2024

 
# your terraform code 
  ```hcl
// Provider configuration
// This block defines the provider as AWS and specifies the region where resources will be created.
provider "aws" {
  region = "us-east-1"
} 
// End of provider block

// EC2 instance provisioning block
// This block provisions an EC2 instance with the specified AMI and instance type.
// It also associates a security group and runs a startup script to serve a simple web page.
resource "aws_instance" "web_server" {
  // Amazon Machine Image (AMI) ID for the instance
  ami                    = "ami-04a81a99f5ec58529"
  
  // EC2 instance type (t2.micro qualifies for the AWS free tier)
  instance_type          = "t2.micro"
  
  // Attach the security group defined below to the instance
  vpc_security_group_ids = [aws_security_group.instance.id]

  // User data script that runs at instance startup
  // It creates an "index.html" file and serves it using BusyBox HTTP server on the specified port
  user_data = <<-EOF
    #!/bin/bash
    echo "Hello, World" > index.html
    nohup busybox httpd -f -p ${var.server_port} &
  EOF

  // Assign a tag to the instance for easier identification
  tags = {
    Name = "web-server-configurable"
  }
}

// Security group block
// This block creates a security group to allow inbound traffic on the specified port.
resource "aws_security_group" "instance" {
  // Name of the security group
  name = "terraform-example-instance"
  
  // Ingress rule allowing inbound traffic
  // It opens the port defined by the server_port variable for all IP addresses (0.0.0.0/0)
  ingress {
    from_port   = var.server_port
    to_port     = var.server_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

// Variable block
// This block defines a variable for the server port with a default value of 8080.
variable "server_port" {
  description = "The port the server will use for HTTP requests"
  type        = number
  default     = 8080
}

// Output block
// This block outputs the public IP address of the EC2 instance after it's created.
output "public_ip" {
  value       = aws_instance.web_server.public_ip
  description = "The public IP address of the web server"
}
