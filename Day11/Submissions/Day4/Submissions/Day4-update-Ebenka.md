# Day 4: Mastering Basic Infrastructure with Terraform


## Participant Details

- **Name:** Ebenka christian joel
- **Date and Time:** 26-08-2024 at 05:13 am 

1. **reading**: Chapter 2 of "Terraform: Up & Running" by Yevgeniy Brikman.
2. **Udemy Videos**: 
   - Rewatch Day 3 videos (Videos 11, 12, and 13).
   - Watch "Input Variables" (Video 14).
   - Watch "Local Variables" (Video 15).

3. **Activity**:
    - Deploying a Highly Available Web App on AWS Using Terraform
    - Explore Terraform's documentation on providers, resource blocks, and workflow. [https://registry.terraform.io/browse/modules?provider=aws]



# Day 4: Deploying complete webserver Infrastructure with Terraform

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

#Create default VPC if one does not exist
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

# Create a secondary subet if does not exist
resource "aws_default_subnet" "default_az2" {
  availability_zone = data.aws_availability_zones.available_zones.names[1]
  tags = {
    Name = "30_days_server2"
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
  subnet_id              = [aws_default_subnet.default_az1.id, aws_default_subnet.default_az2.id][1]
  vpc_security_group_ids = [aws_security_group.web_ec2_security_group.id]
  key_name               = var.aws_key_pair
  user_data              = <<-EOF
  #!/bin/bash
  sudo yum update -y
  sudo yum install httpd -y
  sudo systemctl start httpd
  sudo systemctl enable httpd
  sudo systemctl status httpd
  echo "<h1> Terraform 30 days challenge day4 Ebenka Joel - Hostname: $(hostname) </h1>" | sudo tee -a /var/www/html/index.html
  EOF

  `````

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

3-autoscale.tf:

```bash
##Author: Joel Ebenka
# Create Auto Scaling Group
resource "aws_launch_template" "terraform_temp" {
  name_prefix   = "30_days_Challenge"
  image_id      = "ami-02e136e904f3da870"
  instance_type = var.aws_instance_type
}

# Auto Scaling Group
resource "aws_autoscaling_group" "terraform_group" {
  name               = "Terraform-ASG1"
  desired_capacity   = 2
  max_size           = 5
  min_size           = 2
  target_group_arns   = [aws_lb_target_group.web_tg.arn]
  vpc_zone_identifier = [aws_default_subnet.default_az1.id, aws_default_subnet.default_az2.id]
  launch_template {
    id      = aws_launch_template.terraform_temp.id
    version = "$Latest"
  }
# Required when using a launch configuration with an auto scaling group.
 lifecycle {
    create_before_destroy = true
  }
}


```

4-loadbalancer.tf

```bash
##Author: Joel Ebenka
# Create Application Load Balancer
resource "aws_lb" "web_lb" {
  name               = "web-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web_ec2_security_group.id]
  subnets            = [aws_default_subnet.default_az1.id, aws_default_subnet.default_az2.id]
}

# Create Load Balancer Listener
resource "aws_lb_listener" "web_lb_listener" {
  load_balancer_arn = aws_lb.web_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web_tg.arn
  }
}

# Create Load Balancer Target Group
resource "aws_lb_target_group" "web_tg" {
  name        = "web-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_default_vpc.default_vpc.id
  target_type = "instance"
}

```

5-output.tf:

```bash
# print the url of the webserver
output "ec2_web_url" {
  value     = join ("", ["http://", aws_instance.ec2_instance.public_dns, ":", "80"])
}

# print the url of the webserver
output "ssh_connection_command" {
  value     = join ("", ["ssh -i my_ec2_key.pem ec2-user@", aws_instance.ec2_instance.public_dns])
}




