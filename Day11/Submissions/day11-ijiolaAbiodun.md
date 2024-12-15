# Day 11: Terraform Conditionals



//creating an ASG schedule
resource "aws_autoscaling_schedule" "scale_out_during_business_hours" {
  count = var.enable_autoscaling ? 1 : 0

  scheduled_action_name = "${var.cluster_name}-scale-out-during-business-hours"
  min_size = 2
  max_size = 10
  desired_capacity = 10
  recurrence = "0 9 * * *"
  autoscaling_group_name = aws_autoscaling_group.asg_day.name
}

resource "aws_autoscaling_schedule" "scale_in_at_night" {
  count = var.enable_autoscaling ? 1 : 0
  scheduled_action_name = "${var.cluster_name}-scale-in-at-night"
  min_size = 2
  max_size = 10
  desired_capacity = 2
  recurrence = "0 17 * * *"
  autoscaling_group_name = aws_autoscaling_group.asg_night.name
}


main.tf in production

module "webserver_cluster" {
  source = "../../../modules/prod/aws-scaling-terraform"

  cluster_name = "webservers-stage"
  db_remote_state_bucket = "(my-bucket-${random)"
  db_remote_state_key = "prod/data-stores/mysql/terraform.tfstate"
  enable_autoscaling = true

  //instance_type = "m4.large"
  min_size = 2
  max_size = 10
}
