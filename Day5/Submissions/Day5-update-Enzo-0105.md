# Day 5: Scaling Infrastructure

## Participant Details

- **Name:** Salako Lateef
- **Task Completed:** Mastering Basic Infrastructure with Terraform
- **Date and Time:** 2024-10-2 08:54 PM GMT

## main.tf
```
provider "aws" {
  region = var.region
}
variable "instance_type" {
  description = "EC2 instance to deploy"
  default     = "t2.micro"
}

variable "ami_id" {
  description = "Amazon Machine Image (AMI) ID"
  default     = "ami-0e86e20dae9224db8"
}

variable "subnets" {
  description = "List of Subnets"
  default     = ["subnet-0b80d1672c1d6452a", "subnet-0846e4641e585a3df"]
}

variable "security_group" {
  description = "Security group"
  default     = "sg-0c393266741c7f06a"
}

variable "num_instances" {
  description = "Number of instances in the cluster"
  default     = 2
}

variable "vpc_id" {
  description = "VPC ID"
  default     = "vpc-03a402beb079dd496"
}
data "aws_ami" "web" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["ubuntu/*"]
  }
}

locals {
  name = "web-server"
  Terraform = "true"
  Environment = var.env 
}

locals {
  common_tags = {
    Name = local.name
    Terraform = local.Terraform
    Environment = local.Environment
  }
}

#Creating Application Loadbalancer 
resource "aws_lb" "web-lb" {
  name               = "web-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web-sg.id]
  subnets            = [aws_subnet.public-sub.id, aws_subnet.public-sub1.id]
}

resource "aws_lb_listener" "lb-listener" {
  load_balancer_arn = aws_lb.web-lb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.lb-target.arn
  }
}
resource "aws_lb_target_group" "lb-target" {
  name        = "web-lb-target"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.vpc.id
  target_type = "instance"
}

resource "aws_launch_template" "instance-con" {
  instance_type = "t2.micro"
  image_id      = data.aws_ami.web.id
  #vpc_security_group_ids = [ aws_security_group.web-sg.id ]
  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.web-sg.id]
  }

  user_data = base64encode(<<EOF
#!/bin/bash
sudo apt update -y
sudo apt install nginx -y 
sudo systemctl start nginx 
EOF
  )
}

resource "aws_autoscaling_group" "webscalling" {
  name                = "web-scalling"
  min_size            = 1
  desired_capacity    = var.num_instances
  max_size            = var.num_instances 
  vpc_zone_identifier = [aws_subnet.public-sub.id, aws_subnet.public-sub1.id]
  launch_template {
    id      = aws_launch_template.instance-con.id
    version = "$Latest"
  }

  target_group_arns = [aws_lb_target_group.lb-target.arn]
}

resource "aws_instance" "web-server" {
  ami                         = data.aws_ami.web.id
  subnet_id                   = var.subnets
  instance_type               = var.instance_type
  security_groups             = [aws_security_group.web-sg.id]
  associate_public_ip_address = "true"

  user_data = <<-EOF
  #!/bin/bash 
  sudo apt update -y
  sudo apt install apache2 -y 
  sudo systemctl start apache2 
  EOF

  tags = local.common_tags
}

```

## modules.tf

```
module "instance" {
  source = "../module"
  instance = "t2.micro"
  ami      = data.aws_ami.web.id
  sub      = "subnet-03cb68d25e5198c95"
  key      = "minikube"
  sg       = ["sg-0ed7b0e6d5df0a363"]
}
```
