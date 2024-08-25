 # Day4: Mastering Basic Infrastructure with Terraform

## Participant Details
- **Name:** Nadeem Taj
- **Task Completed:** Deployed both configurable and clustered web servers, reviewed documentation and started creating blog detailing the procedure
- **Date and Time:** 8/21/2024 11:46 PM

 
# Terraform Code - Deploying a Configurable Web Server

I deployed configurable web server using terraform. I have a lot variable in separate file named variable.tf and use these variable in my main.tf file to configured my infrastructure. 


### main.tf

```hcl
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

```hcl
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


### Terraform: Deploy a configurable server clustered 

```hcl

# Define the AWS provider and the region where the resources will be created
provider "aws" {
  region = "us-east-1"
}

# Create a Launch Template for the EC2 instances
resource "aws_launch_template" "terraform_instance" {
  # Specify the Amazon Machine Image (AMI) to use for the instances
  image_id = "ami-04a81a99f5ec58529"
  
  # Specify the instance type for the instances
  instance_type = "t2.micro"
  
  # Associate the Security Group with the instances
  vpc_security_group_ids = [aws_security_group.instance.id]
  
  # Specify the user data script to be executed when the instances are launched
  user_data = base64encode(<<-EOF
#!/bin/bash
echo "Hello, World" > index.html
nohup busybox httpd -f -p ${var.server_port} &
EOF
  )

  # Ensure that a new instance is created before the old one is destroyed
  lifecycle {
    create_before_destroy = true
  }
}

# Create a Security Group to allow incoming traffic on the server port
resource "aws_security_group" "instance" {
  name = "terraform-example-instance407"

  # Allow incoming traffic on the server port from any IP address
  ingress {
    from_port   = var.server_port
    to_port     = var.server_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Define a variable for the server port
variable "server_port" {
  description = "The port the server will use for HTTP requests"
  type        = number
  default     = 8080
}

# Create an Auto Scaling Group (ASG) to manage the instances
resource "aws_autoscaling_group" "terraform_instance" {
  name = "terraform-asg-terraform_instance-407"

  # Use the Launch Template to define the instances in the ASG
  launch_template {
    id      = aws_launch_template.terraform_instance.id
    version = "$Latest"
  }

  # Launch the instances in the default subnets of the default VPC
  vpc_zone_identifier = data.aws_subnets.default.ids

  # Set the minimum and maximum number of instances in the ASG
  min_size = 2
  max_size = 10

  # Tag the instances with a name
  tag {
    key                 = "name"
    value               = "terraform-asg-terraform_instance"
    propagate_at_launch = true
  }
}

# Fetch information about the default VPC
data "aws_vpc" "default" {
  default = true
}

# Fetch information about the default subnets in the default VPC
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Fetch information about the instances in the Auto Scaling Group
data "aws_instances" "asg_instances" {
  filter {
    name   = "tag:name"
    values = ["terraform-asg-terraform_instance"]
  }
}

# Output the public IP addresses of the instances in the Auto Scaling Group
output "public_ips" {
  value       = data.aws_instances.asg_instances.public_ips
  description = "Public IP addresses of the instances in the Auto Scaling Group"
}

# Output the private IP addresses of the instances in the Auto Scaling Group
output "private_ips" {
  value       = data.aws_instances.asg_instances.private_ips
  description = "Private IP addresses of the instances in the Auto Scaling Group"
}

```