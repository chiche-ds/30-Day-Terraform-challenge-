# stage/Data-store/mysql/main.tf

provider "aws" {
region = "us-east-2"
}
resource "aws_db_instance" "example" {
identifier_prefix = "terraform-up-and-running"
engine = "mysql"
allocated_storage = 10
instance_class = "db.t2.micro"
skip_final_snapshot = true
db_name = "example_database"
# How should we set the username and password?
username = var.db_username
password = var.db_password
}

# stage/Data-store/mysql/variable.tf
variable "db_username" {
description = "The username for the database"
type = string
sensitive = true
}
variable "db_password" {
description = "The password for the database"
type = string
sensitive = true
}

# stage/services/webserver-cluster
data "terraform_remote_state" "db" {
backend = "s3"
config = {
bucket = var.db_remote_state_bucket
key = var.db_remote_state_key
region = "us-east-1"
}
}

module "webserver_cluster" {
source = "../../../modules/services/webserver-cluster"
cluster_name = var.cluster_name
db_remote_state_bucket = var.db_remote_state_bucket
db_remote_state_key = var.db_remote_state_key

instance_type = "t2.micro"
min_size = 2
max_size = 2
}

resource "aws_launch_configuration" "example" {
image_id = "ami-0fb653ca2d3203ac1"
instance_type = var.instance_type
security_groups = [aws_security_group.instance.id]
user_data = templatefile("user-data.sh", {
server_port = var.server_port
db_address = data.terraform_remote_state.db.outputs.address
db_port = data.terraform_remote_state.db.outputs.port
})
# Required when using a launch configuration with an auto scaling group.
lifecycle {
create_before_destroy = true
}
}

resource "aws_autoscaling_group" "example" {
launch_configuration = aws_launch_configuration.example.name
vpc_zone_identifier = data.aws_subnets.default.ids
target_group_arns = [aws_lb_target_group.asg.arn]
health_check_type = "ELB"
min_size = var.min_size
max_size = var.max_size
tag {
key = "Name"
value = var.cluster_name
propagate_at_launch = true
}
}

locals {
http_port = 80
any_port = 0
any_protocol = "-1"
tcp_protocol = "tcp"
all_ips = ["0.0.0.0/0"]
}

resource "aws_lb_listener" "http" {
load_balancer_arn = aws_lb.example.arn
port = local.http_port
protocol = "HTTP"
# By default, return a simple 404 page
default_action {
type = "fixed-response"
fixed_response {
content_type = "text/plain"
message_body = "404: page not found"
status_code = 404
}
}
}


resource "aws_security_group" "alb" {
name = "${var.cluster_name}-alb"
}
resource "aws_security_group_rule" "allow_http_inbound" {
type = "ingress"
security_group_id = aws_security_group.alb.id
from_port = local.http_port
to_port = local.http_port
protocol = local.tcp_protocol
cidr_blocks = local.all_ips
}
resource "aws_security_group_rule" "allow_all_outbound" {
type = "egress"
security_group_id = aws_security_group.alb.id
from_port = local.any_port
to_port = local.any_port
protocol = local.any_protocol
cidr_blocks = local.all_ips
}



resource "aws_autoscaling_schedule" "scale_out_during_business_hours" {
    autoscaling_group_name = var.autoscaling_group_name
scheduled_action_name = "scale-out-during-business-hours"
min_size = var.min_size
max_size = var.max_size
desired_capacity = 10
recurrence = "0 9 * * *"
}
resource "aws_autoscaling_schedule" "scale_in_at_night" {
        autoscaling_group_name = var.autoscaling_group_name
scheduled_action_name = "scale-in-at-night"
min_size = 2
max_size = 10
desired_capacity = 2
recurrence = "0 17 * * *"
}


# stage/services/webserver-cluster/output.tf
output "autoscaling_group_name" {
value = aws_autoscaling_group.example.name
description = "The name of the Auto Scaling Group"
}

output "alb_dns_name" {
value = module.webserver_cluster.alb_dns_name
description = "The domain name of the load balancer"
}

# stage/services/webserver-cluster/variable.tf
variable "cluster_name" {
description = "The name to use for all the cluster resources"
type = string
}

variable "db_remote_state_bucket" {
description = "The name of the S3 bucket for the database's remote state"
type = string
}

variable "db_remote_state_key" {
description = "The path for the database's remote state in S3"
type = string
}

variable "instance_type" {
description = "The type of EC2 Instances to run (e.g. t2.micro)"
type = string
}

variable "min_size" {
description = "The minimum number of EC2 Instances in the ASG"
type = number
}

variable "max_size" {
description = "The maximum number of EC2 Instances in the ASG"
type = number
}

variable "server_port" {
    description = " the server port"
    type = number
}

variable "autoscaling_group_name" {
    description = "autoscaling_group_name"
    type = string
}




