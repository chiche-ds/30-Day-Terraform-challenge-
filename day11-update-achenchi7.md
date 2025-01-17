# Day 11: Terraform Conditionals

## Participant Details

- **Name:** Jully Achenchi
- **Task Completed:** Terraform conditionals 
- **Date and Time:** 23/12/2024

## Conditional Resource Deployment with count
Checks if the resource is in dev or production
it then scales if production according to snippet below.


```hcl
resource "aws_autoscaling_schedule" "scale_out_during_business_hours" {
  count = var.enable_autoscaling ? 1 : 0

  scheduled_action_name = "${var.cluster_name}-scale-out-during-business-hours"
  min_size = 2
  max_size = 10
  desired_capacity = 10
  recurrence = "0 9 * * *"
  autoscaling_group_name = aws_autoscaling_group.example.name
}

resource "aws_autoscaling_schedule" "scale_in_at_night" {
  count = var.enable_autoscaling ? 1 : 0
  scheduled_action_name = "${var.cluster_name}-scale-in-at-night"
  min_size = 2
  max_size = 10
  desired_capacity = 2
  recurrence = "0 17 * * *"
  autoscaling_group_name = aws_autoscaling_group.example.name
}
```

main.tf in production
```hcl
module "webserver_cluster" {
  source = "/home/ephantus/Desktop/Terraform/Terraform-up-and-running-pdf/chapter4/modules/services/webserver-cluster"

  cluster_name = "webservers-stage"
  db_remote_state_bucket = "(your_bckt_name)"
  db_remote_state_key = "prod/data-stores/mysql/terraform.tfstate"
  enable_autoscaling = true

  //instance_type = "m4.large"
  min_size = 2
  max_size = 10
}
```
