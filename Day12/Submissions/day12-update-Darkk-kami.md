# Day 12:Zero downtime deplyment using terraform

## Participant Details

- **Name:** Dwayne Chima
- **Task Completed:** Use Terraform to deploy infrastructure updates with zero downtime using techniques like blue/green deployments.
- **Date and Time:** 13th Dec 2024 2:00pm

## Terraform Code 
### **rolling update**
![rolling](https://github.com/user-attachments/assets/edcbff48-c3f4-4070-8392-c34b2c2f4c4d)


**AWS Auto Scaling Groups (ASG)** and **Instance Refresh** to gradually replace old instances while keeping the service running. Here’s how we approached it:

1. **Launch Template**: Created a launch template to define the EC2 instance configuration, including instance type, AMI, and security groups. dentifiable and updated.
   
2. **Application Load Balancer (ALB)**: The ALB is set up to handle traffic and route requests to the target group associated with the ASG. 

3. **Auto Scaling Group**: The ASG is configured with a **rolling update strategy** for instance replacement. We set the `min_healthy_percentage` to 25, meaning the ASG will maintain at least 25% of instances in a healthy state while new instances are brought online. 

```hcl
resource "aws_launch_template" "launch_template" {
  name = "my_launch_template"

  disable_api_stop        = true
  disable_api_termination = true

  ebs_optimized = true

  image_id = data.aws_ami.ubuntu.id

  instance_initiated_shutdown_behavior = "terminate"

  instance_type = var.instance_type

  vpc_security_group_ids = [var.web_sg.id]

  tag_specifications {
    resource_type = "instance"

    tags = {
      Name = "${var.tag}"
    }
  }

  # user script to output the instance's hostname
  user_data = base64encode(templatefile("${path.module}/../../templates/user_data.sh", {
  server_text = "${var.server_text} - ${timestamp()}"
}))
}

resource "aws_lb" "alb" {
  name               = "web-server-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [for subnet in var.public_subnets : subnet.id]
}

resource "aws_lb_target_group" "asg_target_group" {
  name     = "asg-target-group"
  port     = var.inbound_ports[0]
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path                = "/"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }
}

resource "aws_lb_listener" "http_lisener" {
  load_balancer_arn = aws_lb.alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
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

  #
  instance_refresh {
    strategy = "Rolling"

    preferences {
      min_healthy_percentage = 25
    }
  }
  target_group_arns         = [aws_lb_target_group.asg_target_group.arn]
  launch_template {
    id      = aws_launch_template.launch_template.id
    version = aws_launch_template.launch_template.latest_version
  }
  vpc_zone_identifier = [for subnet in var.public_subnets : subnet.id]
}
```
### **Canary update**
![canary](https://github.com/user-attachments/assets/3a4ec99d-5aeb-412a-948b-c7ed5a4d87db)
Implemented traffic routing to test new versions of the application on a small subset of users before gradually shifting all traffic. 

1. **Two Target Groups**: Created one target group for the stable version (`asg_target_group`) and another for the canary version (`canary_target_group`).

2. **Listener Rule for Canary Release**: Configured an ALB listener rule to forward 10% of traffic to the canary target group and 90% to the stable target group. 
```
resource "aws_lb_target_group" "asg_target_group" {
  name     = "asg-target-group"
  port     = var.inbound_ports[0]
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path                = "/"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }
}

resource "aws_lb_target_group" "canary_target_group" {
  name     = "canary-target-group"
  port     = var.inbound_ports[0]
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path                = "/"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }
}


resource "aws_lb_listener_rule" "canary_rule" {
  listener_arn = aws_lb_listener.alb.arn

  condition {
    field  = "path-pattern"
    values = ["/*"]
  }

  action {
    type = "forward"

    forward {
      target_group {
        arn    = aws_lb_target_group.canary_target_group.arn
        weight = 10
      }

      target_group {
        arn    = aws_lb_target_group.asg_target_group.arn
        weight = 90
      }
    }
  }
}
```


