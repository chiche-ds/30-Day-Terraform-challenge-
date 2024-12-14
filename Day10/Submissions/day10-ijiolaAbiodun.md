resource "aws_iam_user" "user" {
  name = var.user_name.id
}

module "users" {
  source = ".././../modules/landing-zone/iam-user"

  count     = length(var.user_name)
  user_name = var.user_names[count.index]
}

resource "aws_autoscaling_group" "example" {
  launch_configuration = aws_launch_configuration.example.name
  vpc_zone_identifier  = data.aws_subnets.default.ids
  target_group_arns    = [aws_lb_target_group.asg.arn]
  health_check_type    = "ELB"
  min_size             = var.min_size
  max_size             = var.max_size
  tag {
    key                 = "Name"
    value               = var.cluster_name
    propagate_at_launch = true
  }
}
