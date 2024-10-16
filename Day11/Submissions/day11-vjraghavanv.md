# Day 11: Terraform Conditionals

## Participant Details

- **Name:** Vijayaraghavan Vashudevan
- **Task Completed:** Learnt - How to implement conditional logic with your Terraform configurations to control resource deployments
- **Date and Time:** 11-09-2024 at 08:27 am IST

## Terraform Code Snippet -Conditional Resource Deployment with count
Auto Scaling will only be deployed if the enable_autoscaling variable is set to true.

```hcl
resource "aws_autoscaling_schedule" "scale_out_during_business_hours" {
  count = var.enable_autoscaling ? 1 : 0
  scheduled_action_name  = "${var.cluster_name}-scale-out-during-business-hours"
  min_size = 2              
  max_size = 10              
  desired_capacity  = 10      
  recurrence = "0 9 * * *"             
  autoscaling_group_name = aws_autoscaling_group.example.name
 }

```

