# Day 11: Terraform Conditionals 

## Participant Details

- **Name:** Franklin Afolabi
- **Task Completed:** Learnt how to implement conditional logic using `count`, `for_each` and `if` in a ternary syntax and why `count` is more powerful.
- **Date and Time:** September 20 1455hrs

## Terraform Code 
```hcl
# Updates to the variable file

variable "custom_tags" {
  description = "Custom tags to set on the Instances in the ASG"
  type = map(string)
  default = {}
}

variable "enable_autoscaling" {
  description = "if set to true, enable auto scaling"
  type = bool
}


# Update to module's main.tf

resource "aws_autoscaling_schedule" "scale_out_during_business_hours" {
    count = var.enable_autoscaling ? 1 : 0

    scheduled_action_name = "${var.cluster_name}-scale_out_during_business_hours"
    min_size = 2
    max_size = 10
    desired_capacity = 10
    recurrence = "0 9 * * *"

    autoscaling_group_name = aws_autoscaling_group.example.name
}

resource "aws_autoscaling_schedule" "scale_in_at_night" {
    count = var.enable_autoscaling ? 1 : 0
    scheduled_action_name = "${var.cluster_name}-scale_in_at_night"
    min_size = 2
    max_size = 10
    desired_capacity = 2
    recurrence = "0 17 * * *"

    autoscaling_group_name = aws_autoscaling_group.example.name
}

```
## Architecture 

[Name](link to image in S3 bucket)
