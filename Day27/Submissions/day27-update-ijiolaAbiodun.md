 days/day26/ijiolaAbiodun
resource "aws_autoscaling_schedule" "scale_out_during_business_hours" {
  count = var.enable_autoscaling ? 1 : 0

  scheduled_action_name = "${var.cluster_name}-scale-out-during-business-hours"
  min_size             = 2
  max_size             = 10
  desired_capacity     = 10
  recurrence           = "0 9 * * *" # Cron for 9:00 AM
  autoscaling_group_name = aws_autoscaling_group.asg_day.name
}
resource "aws_autoscaling_schedule" "scale_in_at_night" {
  count = var.enable_autoscaling ? 1 : 0

  scheduled_action_name = "${var.cluster_name}-scale-in-at-night"
  min_size             = 2
  max_size             = 10
  desired_capacity     = 2
  recurrence           = "0 17 * * *" # Cron for 5:00 PM
  autoscaling_group_name = aws_autoscaling_group.asg_night.name
}
variable "enable_autoscaling" {
  description = "If set to true, enable auto scaling"
  type        = bool
}module "webserver_cluster" {
  source = "../../../modules/prod/aws-scaling-terraform"

  cluster_name           = "webservers-stage"
  db_remote_state_bucket = "my-production-bucket"
  db_remote_state_key    = "prod/data-stores/mysql/terraform.tfstate"
  enable_autoscaling     = true

  min_size = 2
  max_size = 10
}

https://github.com/Stormz99/aws-scaling-and-monitoring-terraform.git


