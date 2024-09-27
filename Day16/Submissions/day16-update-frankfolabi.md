# Day 16: Building Production-Grade Infrastructure 

## Participant Details

- **Name:** Franklin Afolabi
- **Task Completed:** Created composable modules that are easy for testing. Installed tfenv for Terraform versions management. Worked on validations, preconditons and postconditions. Learnt on how to create terraform-aws-modules on the public Terraform registry. Worked with provisioners and external data. To avoid many lines Terraforn code of each module, only the main modules are included in this submission.
- **Date and Time:** September 27 1432

## Terraform Code 
```hcl

provider "aws" {
    region = "us-east-2"
}

module "hello_world_app" {
    source = "github.com/frankfolabi/terraform-up-and-running//challenge/modules/services/webserver-cluster?ref=v0.0.2"

    server_text = "New server text"
    environment = "stage"
    db_remote_state_bucket = "tf-frankfolabi"
    db_remote_state_key = "stage/data-stores/mysql/terraform.tfstate"

   
    instance_type = "t2.micro"

    min_size = 2
    max_size = 2 
    enable_autoscaling = false

     ami =data.aws_ami.ubuntu.id
    subnet_ids = data.aws_subnets.default.ids
}

data "aws_vpc" "default" {
    default = true
}

data "aws_subnets" "default" {
    filter {
        name = "vpc-id"
        values = [data.aws_vpc.default.id]
    }
}

data "aws_ami" "ubuntu" {
    most_recent = true
    owners = ["099720109477"]

    filter {
        name = "name"
        values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
    }
}

------------------------------------------------------------------------------------
## outputs.tf


output "alb_dns_name" {
    value = module.hello_world_app.alb_dns_name
    description = "The domain name of the load balancer"
}
-------------------------------------------------------------------------------------
## hello-app module which contains other composable modules

# Define data sources
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
    filter {
      name = "vpc-id"
      values = [data.aws_vpc.default.id]
    }
}

data "terraform_remote_state" "db" {
  backend = "s3"

  config = {
    bucket = var.db_remote_state_bucket
    key = var.db_remote_state_key
    region = "us-east-2"
  }
}


# Create target group for auto scaling group
resource "aws_lb_target_group" "asg" {
  name = "hello-world-${var.environment}"
  port =  var.server_port
  protocol = "HTTP"
  vpc_id = data.aws_vpc.default.id

  health_check {
    path = "/"
    protocol = "HTTP"
    matcher = "200"
    interval = 15
    timeout = 3
    healthy_threshold = 2
    unhealthy_threshold = 2
  }
}

# Create the ALB listerner rules
resource "aws_lb_listener_rule" "asg" {
  listener_arn = module.alb.alb_http_listener_arn
  priority = 100

  condition {
    path_pattern {
      values = ["*"]
    }
  }
  action {
    type = "forward"
    target_group_arn = aws_lb_target_group.asg.arn
  }
}


module "asg" {
    source = "../../cluster/asg-rolling-deploy"

    cluster_name = "hello-world-${var.environment}"
    ami = var.ami
    instance_type = var.instance_type

    user_data = templatefile("${path.module}/user-data.sh", {
        server_port = var.server_port
        db_address = data.terraform_remote_state.db.outputs.address
        db_port = data.terraform_remote_state.db.outputs.port
        server_text = var.server_text
    })

    min_size = var.min_size
    max_size = var.max_size
    enable_autoscaling = var.enable_autoscaling

    subnet_ids = data.aws_subnets.default.ids
    target_group_arns = [aws_lb_target_group.asg.arn]
    health_check_type = "ELB"

    custom_tags = var.custom_tags
}


module "alb" {
    source = "../../networking/alb"

    alb_name = "hello-world-${var.environment}"
    subnet_ids = data.aws_subnets.default.ids

    
}



```
## Architecture 

[Name](link to image in S3 bucket)
