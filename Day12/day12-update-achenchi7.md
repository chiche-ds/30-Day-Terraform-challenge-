# Day 11: Terraform Zero-Downtime Deployment


## Participant Details

- **Name:** Jully Achenchi
- **Task Completed:** Understood Terraform Zero-Downtime Deployment
- **Date and Time:** 26/12/2024

## Zero-Downtime Deployment
1. Configure the name parameter of the Auto-scaling-group to depend directly on the name of the
launch configuration.
2. Set the create_before_destroy parameter of ASG to true.
3. Set min_elb_capacity of the ASG to min_size of cluster for terraform to wait until many servers pass health check before destroying the original.
   


```hcl
resource "aws_autoscaling_group" "example" {
  # Explicitly depend on the launch configuration's name so each time it's
  # replaced, this ASG is also replaced
  name = "${var.cluster_name}-${aws_launch_configuration.example.name}"
  
  launch_configuration = aws_launch_configuration.example.name
  vpc_zone_identifier  = data.aws_subnets.default.ids

  target_group_arns = [aws_lb_target_group.asg.arn]
  health_check_type = "ELB"

  min_size = var.min_size
  max_size = var.max_size

  # Wait for at least this many instances to pass health checks before
  # considering the ASG deployment complete
  min_elb_capacity = var.min_size

  # When replacing this ASG, create the replacement first, and only delete the
  # original after
  lifecycle {
    create_before_destroy = true
  }

  tag {
    key                 = "Name"
    value               = "terraform-asg-example"
    propagate_at_launch = true
  }
}
```
After min_elb_capacity servers from the v2 ASG cluster have registered in the ALB,
Terraform will begin to terminate the old ASG
