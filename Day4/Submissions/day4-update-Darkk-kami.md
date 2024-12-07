# Day 4: Mastering Basic Infrastructure with Terraform
* Name: Dwayne Chima
* Task Completed: Mastering basic infrastructure with terraform
Date: 5th Dec 4:30pm


## Architecture Diagram
![asg](https://github.com/user-attachments/assets/c7cbeef3-09d2-4ae9-a33c-2f880be6684f)

**main.tf**
```
resource "aws_vpc" "vpc" {
  cidr_block = var.cidr
  instance_tenancy = "default"
  tags = {
    Name = "${var.tag}-vpc"
  }
}

data "aws_availability_zones" "available" {}

resource "aws_subnet" "private_subnets" {
  count                   = var.public_subnets_no
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = cidrsubnet(var.cidr, 8, count.index) 
  availability_zone       = tolist(data.aws_availability_zones.available.names)[count.index]
  map_public_ip_on_launch = false
  tags                    = {
    Name = "${var.tag}-private-subent-${count.index}"
  }
}

resource "aws_subnet" "public_subnets" {
  count                   = var.public_subnets_no
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = cidrsubnet(var.cidr, 8, count.index + 100) 
  availability_zone       = tolist(data.aws_availability_zones.available.names)[count.index]
  map_public_ip_on_launch = true
  tags                    = {
    Name = "${var.tag}-public-subent-${count.index}"
  }
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "${var.tag}-igw"
  }
}

resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
  }

  tags = {
    Name = "${var.tag}-public-route-table"
  }
}

# Associate public subnets with the route table
resource "aws_route_table_association" "public_route_table_association" {
  depends_on     = [aws_subnet.public_subnets]
  route_table_id = aws_route_table.public_route_table.id
  for_each       = { for idx, subnet in aws_subnet.public_subnets : idx => subnet }
  subnet_id      = each.value.id
}


resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "${var.tag}-private-route-table"
  }
}

resource "aws_route_table_association" "private" {
  depends_on     = [aws_subnet.private_subnets]
  route_table_id = aws_route_table.private_route_table.id
  for_each       = { for idx, subnet in aws_subnet.private_subnets : idx => subnet }
  subnet_id      = each.value.id
}


# ..........................Security Groups................................. #
resource "aws_security_group" "web_sg" {
  name        = "web_sg"
  description = "Allow alb traffic inbound and outbound"
  vpc_id      = aws_vpc.vpc.id
  tags = {
    Name = "${var.tag}-sg"
  }
}


resource "aws_vpc_security_group_ingress_rule" "allow_http" {
  for_each          = { for idx, port in var.inbound_ports : idx => port } 
  security_group_id = aws_security_group.web_sg.id
  referenced_security_group_id = aws_security_group.alb_sg.id
  from_port         = each.value
  to_port           = each.value
  ip_protocol       = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "app_allow_all_outbound" {
  security_group_id = aws_security_group.web_sg.id
  cidr_ipv4         = "0.0.0.0/0"  
  ip_protocol       = "-1"         
}


# ..........................Web server................................. #

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd*/ubuntu-*-${var.distro_version}-amd64-server-*"]
  }

  owners = ["099720109477"]  
}

```

**lt.tf**
```
resource "aws_launch_template" "launch_template" {
  name = "my_launch_template"

  disable_api_stop        = true
  disable_api_termination = true

  ebs_optimized = true

  image_id = data.aws_ami.ubuntu.id

  instance_initiated_shutdown_behavior = "terminate"

  instance_type = "t2.micro"

  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tag_specifications {
    resource_type = "instance"

    tags = {
      Name = "${var.tag}"
    }
  }
  
  # user script to output the instance's hostname
  user_data = base64encode(<<-EOT
    #!/bin/bash
    sudo apt update -y
    sudo apt upgrade -y
    sudo apt install -y nginx
    sudo systemctl start nginx
    sudo systemctl enable nginx
    echo "<h1>Hello from Terraform at $(hostname -f)</h1>" | sudo tee /var/www/html/index.html
  EOT
  )
}

resource "aws_security_group" "alb_sg" {
  description = "Allow TLS traffic inbound and all outbound"
  vpc_id      = aws_vpc.vpc.id
  tags = {
    Name = "${var.tag}-sg"
  }
}


resource "aws_vpc_security_group_ingress_rule" "allow_http_alb" {
  for_each          = { for idx, port in var.inbound_ports : idx => port } 
  security_group_id = aws_security_group.alb_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = each.value
  to_port           = each.value
  ip_protocol       = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "app_allow_all_outbound_alb" {
  security_group_id = aws_security_group.alb_sg.id
  cidr_ipv4         = "0.0.0.0/0"  
  ip_protocol       = "-1"         
}


resource "aws_lb" "alb" {  
  name = "web-server-alb"
  internal = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.alb_sg.id]
  subnets = [for subnet in aws_subnet.public_subnets: subnet.id]
}

resource "aws_lb_target_group" "asg_target_group" {
  name = "asg-target-group"
  port = 80
  protocol = "HTTP"
  vpc_id = aws_vpc.vpc.id

  health_check {
    path = "/"
    interval = 30
    timeout = 5
    healthy_threshold = 3
    unhealthy_threshold = 3
  }
}

resource "aws_lb_listener" "http_lisener" {
  load_balancer_arn = aws_lb.alb.arn
  port = 80
  protocol = "HTTP"

  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.asg_target_group.arn
  }
}

## autoscaling group
resource "aws_autoscaling_group" "web_asg" {
  name                      = "Web_server_asg"
  max_size                  = 3
  min_size                  = 3
  health_check_grace_period = 300
  health_check_type         = "ELB"
  desired_capacity          = 3
  force_delete              = true
  target_group_arns = [aws_lb_target_group.asg_target_group.arn]
  launch_template {
    id      = aws_launch_template.launch_template.id
    version = "$Latest"
  }
  vpc_zone_identifier       = [for subnet in aws_subnet.public_subnets : subnet.id]
}

output "alb_dns" {
  value = aws_lb.alb.dns_name
}

```

**varaiables.tf**
```
variable "region" {
  default = "us-east-1"
}


variable "tag" {
  type = string
  default = "webserver"
}

variable "cidr" {
  description = "This is the Cidr block of he vpc"
  type = string
  default = "10.0.0.0/16"
}

variable "private_subnets_no" {
  description = "This is the number of Private subnets"
  type = number
  default = 1
}

variable "public_subnets_no" {
  description = "this is the numer of Public subnets"
  type = number
  default = 3
}

variable "inbound_ports" {
  description = "This is the ports open for inbound trafic"
  type = list(string)
  default = [ "80" ]
}

variable "distro_version" {
  type = string
  default = "24.04"
}

variable "instance_type" {
  type = string
  default = "t2.micro"
}
```
